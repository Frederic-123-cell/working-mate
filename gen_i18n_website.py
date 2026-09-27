# -*- coding: utf-8 -*-
"""
官网「真实界面实拍」区块的多语言文案（18 key × 9 语言）。

用法：  python gen_i18n_website.py
说明：  合并式写入 —— 只在 lang.<code>.js 的最后一个键之后追加，不覆盖任何既有条目。
        末尾键若无逗号会自动补上（JS 语法要求，之前踩过这个坑）。
"""
import io, json, os, re, sys

LANGS = ["en", "ja", "ko", "fr", "de", "ru", "ar", "es", "pt"]

DATA = {
    # ── 登录页（login.html）──
    "login.docTitle": {
        "en": "Sign in / Sign up — Working Mate",
        "ja": "ログイン / 新規登録 — Working Mate",
        "ko": "로그인 / 회원가입 — Working Mate",
        "fr": "Connexion / Inscription — Working Mate",
        "de": "Anmelden / Registrieren — Working Mate",
        "ru": "Вход / Регистрация — Working Mate",
        "ar": "تسجيل الدخول / إنشاء حساب — Working Mate",
        "es": "Iniciar sesión / Registrarse — Working Mate",
        "pt": "Entrar / Criar conta — Working Mate",
    },
    "login.h1": {
        "en": "Sign in / Sign up",
        "ja": "ログイン / 新規登録",
        "ko": "로그인 / 회원가입",
        "fr": "Connexion / Inscription",
        "de": "Anmelden / Registrieren",
        "ru": "Вход / Регистрация",
        "ar": "تسجيل الدخول / إنشاء حساب",
        "es": "Iniciar sesión / Registrarse",
        "pt": "Entrar / Criar conta",
    },
    "login.sub": {
        "en": "No password needed — use a code or a third-party account, and a new account is created automatically.",
        "ja": "パスワード不要。認証コードか外部アカウントで、新規アカウントは自動作成されます。",
        "ko": "비밀번호가 필요 없습니다. 인증 코드나 외부 계정으로 로그인하면 새 계정이 자동 생성됩니다.",
        "fr": "Aucun mot de passe : un code ou un compte tiers suffit, le compte est créé automatiquement.",
        "de": "Kein Passwort nötig – nutze einen Code oder ein Drittanbieter-Konto; ein neues Konto wird automatisch angelegt.",
        "ru": "Пароль не нужен: используйте код или сторонний аккаунт — новый аккаунт создаётся автоматически.",
        "ar": "لا حاجة إلى كلمة مرور: استخدم رمزًا أو حسابًا خارجيًا، ويُنشأ حساب جديد تلقائيًا.",
        "es": "Sin contraseña: usa un código o una cuenta externa y la cuenta se crea automáticamente.",
        "pt": "Sem senha: use um código ou uma conta externa e a conta é criada automaticamente.",
    },
    "login.or": {
        "en": "or",
        "ja": "または",
        "ko": "또는",
        "fr": "ou",
        "de": "oder",
        "ru": "или",
        "ar": "أو",
        "es": "o",
        "pt": "ou",
    },
    "login.email": {
        "en": "Email address",
        "ja": "メールアドレス",
        "ko": "이메일 주소",
        "fr": "Adresse e-mail",
        "de": "E-Mail-Adresse",
        "ru": "Адрес эл. почты",
        "ar": "البريد الإلكتروني",
        "es": "Correo electrónico",
        "pt": "E-mail",
    },
    "login.phone": {
        "en": "Phone number",
        "ja": "電話番号",
        "ko": "휴대폰 번호",
        "fr": "Numéro de téléphone",
        "de": "Telefonnummer",
        "ru": "Номер телефона",
        "ar": "رقم الهاتف",
        "es": "Número de teléfono",
        "pt": "Número de telefone",
    },
    "login.code": {
        "en": "Verification code",
        "ja": "認証コード",
        "ko": "인증 코드",
        "fr": "Code de vérification",
        "de": "Bestätigungscode",
        "ru": "Код подтверждения",
        "ar": "رمز التحقق",
        "es": "Código de verificación",
        "pt": "Código de verificação",
    },
    "login.phCode": {
        "en": "6-digit code",
        "ja": "6桁のコード",
        "ko": "6자리 코드",
        "fr": "Code à 6 chiffres",
        "de": "6-stelliger Code",
        "ru": "6-значный код",
        "ar": "رمز مكوّن من 6 أرقام",
        "es": "Código de 6 dígitos",
        "pt": "Código de 6 dígitos",
    },
    "login.note": {
        "en": "By signing up you accept the Terms of Service and Privacy Policy. New accounts get 3,000 credits.",
        "ja": "登録すると利用規約とプライバシーポリシーに同意したものとみなされます。新規アカウントには 3000 クレジットを進呈。",
        "ko": "가입 시 서비스 약관과 개인정보 처리방침에 동의한 것으로 간주됩니다. 신규 계정에는 3000 크레딧이 지급됩니다.",
        "fr": "En vous inscrivant, vous acceptez les Conditions d'utilisation et la Politique de confidentialité. Les nouveaux comptes reçoivent 3 000 crédits.",
        "de": "Mit der Registrierung akzeptierst du die Nutzungsbedingungen und die Datenschutzrichtlinie. Neue Konten erhalten 3.000 Credits.",
        "ru": "Регистрируясь, вы принимаете Условия использования и Политику конфиденциальности. Новым аккаунтам — 3000 кредитов.",
        "ar": "بالتسجيل فإنك توافق على شروط الاستخدام وسياسة الخصوصية. وتحصل الحسابات الجديدة على 3000 نقطة.",
        "es": "Al registrarte aceptas los Términos de uso y la Política de privacidad. Las cuentas nuevas reciben 3000 créditos.",
        "pt": "Ao criar a conta você aceita os Termos de Uso e a Política de Privacidade. Contas novas ganham 3000 créditos.",
    },
    "login.account": {
        "en": "Account",
        "ja": "アカウント",
        "ko": "계정",
        "fr": "Compte",
        "de": "Konto",
        "ru": "Аккаунт",
        "ar": "الحساب",
        "es": "Cuenta",
        "pt": "Conta",
    },
    "login.logout": {
        "en": "Sign out",
        "ja": "ログアウト",
        "ko": "로그아웃",
        "fr": "Se déconnecter",
        "de": "Abmelden",
        "ru": "Выйти",
        "ar": "تسجيل الخروج",
        "es": "Cerrar sesión",
        "pt": "Sair",
    },
    "login.backHome": {
        "en": "← Back to site",
        "ja": "← サイトに戻る",
        "ko": "← 사이트로 돌아가기",
        "fr": "← Retour au site",
        "de": "← Zurück zur Website",
        "ru": "← Вернуться на сайт",
        "ar": "← العودة إلى الموقع",
        "es": "← Volver al sitio",
        "pt": "← Voltar ao site",
    },
    "login.freeDownload": {
        "en": "Free download",
        "ja": "無料ダウンロード",
        "ko": "무료 다운로드",
        "fr": "Téléchargement gratuit",
        "de": "Kostenloser Download",
        "ru": "Скачать бесплатно",
        "ar": "تحميل مجاني",
        "es": "Descarga gratuita",
        "pt": "Download gratuito",
    },
    "login.soonTitle": {
        "en": "Sign-in is opening soon",
        "ja": "ログインは近日公開",
        "ko": "로그인 곧 오픈",
        "fr": "La connexion arrive bientôt",
        "de": "Anmeldung bald verfügbar",
        "ru": "Вход скоро откроется",
        "ar": "تسجيل الدخول قريبًا",
        "es": "El inicio de sesión llegará pronto",
        "pt": "Login em breve",
    },
    "login.soonSub": {
        "en": "The account system is in its final integration — for now you can use every local feature without signing up. The desktop app is downloadable today; once sign-in opens, your credits and membership sync to your account automatically.",
        "ja": "アカウントシステムは最終調整中です。今すぐ登録なしでローカル機能をすべて使えます。デスクトップ版は本日ダウンロード可能で、ログイン開始後はクレジットと会員情報が自動でアカウントに同期されます。",
        "ko": "계정 시스템을 최종 점검 중입니다. 지금은 가입 없이 모든 로컬 기능을 사용할 수 있습니다. 데스크톱 앱은 지금 다운로드할 수 있으며, 로그인이 열리면 크레딧과 멤버십이 계정에 자동으로 동기화됩니다.",
        "fr": "Le système de comptes est en cours d'intégration finale : pour l'instant, toutes les fonctions locales sont utilisables sans inscription. L'application de bureau est téléchargeable dès aujourd'hui ; à l'ouverture de la connexion, vos crédits et votre abonnement se synchroniseront automatiquement.",
        "de": "Das Kontosystem wird gerade final integriert – bis dahin kannst du alle lokalen Funktionen ohne Registrierung nutzen. Die Desktop-App ist heute herunterladbar; sobald die Anmeldung öffnet, werden Credits und Mitgliedschaft automatisch mit deinem Konto synchronisiert.",
        "ru": "Система аккаунтов на финальной стадии: пока все локальные функции доступны без регистрации. Десктопное приложение можно скачать уже сегодня; после открытия входа кредиты и подписка синхронизируются с вашим аккаунтом автоматически.",
        "ar": "نظام الحسابات في مرحلة الربط النهائية: يمكنك حاليًا استخدام كل الميزات المحلية دون تسجيل. تطبيق سطح المكتب متاح للتنزيل اليوم، وعند فتح تسجيل الدخول ستُزامَن نقاطك وعضويتك مع حسابك تلقائيًا.",
        "es": "El sistema de cuentas está en su integración final: por ahora puedes usar todas las funciones locales sin registrarte. La app de escritorio ya se puede descargar; cuando se abra el inicio de sesión, tus créditos y tu suscripción se sincronizarán automáticamente.",
        "pt": "O sistema de contas está em integração final: por enquanto você pode usar todos os recursos locais sem se cadastrar. O app para desktop já pode ser baixado; quando o login abrir, seus créditos e sua assinatura serão sincronizados automaticamente.",
    },
    "login.minimal": {
        "en": "Minimal",
        "ja": "ミニマル",
        "ko": "미니멀",
        "fr": "Minimal",
        "de": "Minimal",
        "ru": "Минимализм",
        "ar": "بسيط",
        "es": "Minimalista",
        "pt": "Minimalista",
    },
    "home.nav.shots": {
        "en": "Screenshots", "ja": "画面紹介", "ko": "실제 화면",
        "fr": "Captures", "de": "Screenshots", "ru": "Скриншоты",
        "ar": "لقطات الشاشة", "es": "Capturas", "pt": "Capturas",
    },
    "pricing.per.forever": {
        "en": "forever", "ja": "ずっと無料", "ko": "평생 무료",
        "fr": "à vie", "de": "für immer", "ru": "навсегда",
        "ar": "مدى الحياة", "es": "para siempre", "pt": "para sempre",
    },
    "pricing.per.month": {
        "en": "/ month", "ja": "/ 月", "ko": "/ 월",
        "fr": "/ mois", "de": "/ Monat", "ru": "/ месяц",
        "ar": "/ شهريًا", "es": "/ mes", "pt": "/ mês",
    },
    "pricing.per.usage": {
        "en": "+ usage", "ja": "+ 従量", "ko": "+ 사용량",
        "fr": "+ à l'usage", "de": "+ nach Verbrauch", "ru": "+ по факту",
        "ar": "+ حسب الاستخدام", "es": "+ por uso", "pt": "+ por uso",
    },
    "home.shots.tag": {
        "en": "Real Interface", "ja": "実際の画面", "ko": "실제 화면",
        "fr": "Interface réelle", "de": "Echte Oberfläche", "ru": "Реальный интерфейс",
        "ar": "الواجهة الحقيقية", "es": "Interfaz real", "pt": "Interface real",
    },
    "home.shots.h2": {
        "en": "Not mockups — the real interface",
        "ja": "レンダリングではなく、本物の画面",
        "ko": "렌더링이 아니라 진짜 화면입니다",
        "fr": "Pas des rendus : la vraie interface",
        "de": "Keine Renderings — die echte Oberfläche",
        "ru": "Не рендеры, а настоящий интерфейс",
        "ar": "ليست صورًا مُصطنعة، بل الواجهة الحقيقية",
        "es": "No son renders: es la interfaz real",
        "pt": "Não são renders: é a interface real",
    },
    "home.shots.p": {
        "en": "Every image below is a direct in-app screenshot: no touch-ups, no placeholders. The features are real, and so is the UI.",
        "ja": "以下の画像はすべてアプリ内でそのまま撮影した実写です。美化もプレースホルダーもありません。機能も UI も本物です。",
        "ko": "아래 이미지는 모두 앱 안에서 그대로 캡처한 실사입니다. 보정도, 임시 이미지도 없습니다. 기능도 UI도 진짜입니다.",
        "fr": "Chaque image ci-dessous est une capture directe depuis l'application : aucune retouche, aucun visuel de remplacement. Les fonctions sont réelles, l'interface aussi.",
        "de": "Jedes Bild unten ist ein direkter Screenshot aus der App: keine Retusche, keine Platzhalter. Die Funktionen sind echt, die Oberfläche auch.",
        "ru": "Каждое изображение ниже — прямой скриншот из приложения: без ретуши и заглушек. Функции настоящие, интерфейс тоже.",
        "ar": "كل صورة أدناه لقطة مباشرة من داخل التطبيق: بلا تجميل وبلا صور مؤقتة. الميزات حقيقية والواجهة كذلك.",
        "es": "Todas las imágenes de abajo son capturas directas de la aplicación: sin retoques ni imágenes de relleno. Las funciones son reales y la interfaz también.",
        "pt": "Todas as imagens abaixo são capturas diretas do aplicativo: sem retoques e sem imagens de preenchimento. Os recursos são reais e a interface também.",
    },
    "home.shots.s1t": {
        "en": "Main window · multi-model routing chat",
        "ja": "メイン画面 · マルチモデルルーティング対話",
        "ko": "메인 화면 · 멀티 모델 라우팅 대화",
        "fr": "Fenêtre principale · conversation multi-modèles",
        "de": "Hauptfenster · Multi-Modell-Routing-Chat",
        "ru": "Главное окно · диалог с мультимодельной маршрутизацией",
        "ar": "النافذة الرئيسية · محادثة بتوجيه متعدد النماذج",
        "es": "Ventana principal · chat con enrutado multimodelo",
        "pt": "Janela principal · conversa com roteamento multimodelo",
    },
    "home.shots.s1d": {
        "en": "Drop in one sentence and it picks the best expert and model for the job. Session history and capability nav on the left, live credit balance bottom-right.",
        "ja": "一文を投げるだけで最適な専門家とモデルを自動選択。左は履歴と機能ナビ、右下はクレジット残高がリアルタイム更新。",
        "ko": "한 문장만 넣으면 가장 알맞은 전문가와 모델을 자동으로 고릅니다. 왼쪽은 대화 기록과 기능 내비게이션, 오른쪽 아래는 실시간 크레딧 잔액.",
        "fr": "Une phrase suffit : l'app choisit l'expert et le modèle les plus adaptés. Historique et navigation à gauche, solde de crédits en temps réel en bas à droite.",
        "de": "Ein Satz genügt – die App wählt den passenden Experten und das passende Modell. Links Verlauf und Navigation, unten rechts das Guthaben in Echtzeit.",
        "ru": "Достаточно одной фразы — приложение само выберет эксперта и модель. Слева история и навигация, справа снизу баланс кредитов в реальном времени.",
        "ar": "اكتب جملة واحدة فيختار الخبير والنموذج الأنسب تلقائيًا. يسارًا سجل الجلسات والتنقل، وأسفل اليمين رصيدك يتحدّث لحظيًا.",
        "es": "Basta una frase: elige al experto y al modelo más adecuados. Historial y navegación a la izquierda, saldo de créditos en tiempo real abajo a la derecha.",
        "pt": "Basta uma frase: ele escolhe o especialista e o modelo mais adequados. Histórico e navegação à esquerda, saldo de créditos em tempo real no canto inferior direito.",
    },
    "home.shots.s2t": {
        "en": "Workflow canvas · drag into a pipeline",
        "ja": "ワークフローキャンバス · ドラッグでパイプライン",
        "ko": "워크플로 캔버스 · 드래그로 파이프라인 구성",
        "fr": "Canevas de workflow · glissez pour bâtir un pipeline",
        "de": "Workflow-Canvas · per Drag zur Pipeline",
        "ru": "Канвас процессов · перетащите и соберите конвейер",
        "ar": "لوحة سير العمل · اسحب لتبني خط إنتاج",
        "es": "Lienzo de flujos · arrastra y monta un pipeline",
        "pt": "Tela de fluxos · arraste e monte um pipeline",
    },
    "home.shots.s2d": {
        "en": "Script → shots → video → music. Wire it once, run the whole chain; every node previews on its own.",
        "ja": "脚本 → 絵コンテ → 動画 → 音楽。一度つなげば一気に実行、各ノードは個別にプレビュー可能。",
        "ko": "대본 → 스토리보드 → 영상 → 음악. 한 번 연결하면 한 번에 실행되고, 각 노드는 따로 미리 볼 수 있습니다.",
        "fr": "Scénario → storyboard → vidéo → musique. Câblez une fois, exécutez toute la chaîne ; chaque nœud s'aperçoit séparément.",
        "de": "Skript → Storyboard → Video → Musik. Einmal verbinden, komplett durchlaufen lassen; jeder Knoten lässt sich einzeln ansehen.",
        "ru": "Сценарий → раскадровка → видео → музыка. Соедините один раз и запускайте всю цепочку; каждый узел можно посмотреть отдельно.",
        "ar": "نص → لوحة مشاهد → فيديو → موسيقى. صِلها مرة وشغّل السلسلة كاملة، مع معاينة كل عقدة على حدة.",
        "es": "Guion → storyboard → vídeo → música. Conéctalo una vez y ejecuta toda la cadena; cada nodo se previsualiza por separado.",
        "pt": "Roteiro → storyboard → vídeo → música. Conecte uma vez e rode a cadeia inteira; cada nó tem prévia individual.",
    },
    "home.shots.s3t": {
        "en": "Project Space · an AI PM dispatches the work",
        "ja": "プロジェクトスペース · AI PM が業務を割り振り",
        "ko": "프로젝트 스페이스 · AI PM이 업무 배분",
        "fr": "Espace projet · un chef de projet IA répartit le travail",
        "de": "Projektbereich · ein KI-Projektleiter verteilt die Arbeit",
        "ru": "Пространство проекта · ИИ-руководитель распределяет работу",
        "ar": "مساحة المشروع · مدير مشروع ذكي يوزّع العمل",
        "es": "Espacio de proyecto · un jefe de proyecto IA reparte el trabajo",
        "pt": "Espaço de projeto · um gerente de projeto IA distribui o trabalho",
    },
    "home.shots.s3d": {
        "en": "Set a goal — it breaks the work down, assigns experts, and keeps every artifact and status inside the space.",
        "ja": "目標を設定すると自動でタスク分解し専門家へ割り当て、成果物と進捗はスペース内に残ります。",
        "ko": "목표를 정하면 자동으로 작업을 쪼개 전문가에게 배정하고, 산출물과 진행 상황은 스페이스에 남습니다.",
        "fr": "Fixez un objectif : il découpe les tâches, les confie aux experts et conserve livrables et avancement dans l'espace.",
        "de": "Ziel setzen – die App zerlegt die Arbeit, weist Experten zu und behält Ergebnisse und Status im Bereich.",
        "ru": "Задайте цель — он разобьёт работу на задачи, назначит экспертов и сохранит результаты и статус в пространстве.",
        "ar": "حدّد هدفًا فيفكّكه إلى مهام ويسندها إلى الخبراء، وتبقى المخرجات وحالة التقدّم داخل المساحة.",
        "es": "Define un objetivo y descompone las tareas, las asigna a expertos y guarda entregables y avance dentro del espacio.",
        "pt": "Defina um objetivo e ele divide as tarefas, designa especialistas e mantém entregáveis e progresso dentro do espaço.",
    },
    "home.shots.s4t": {
        "en": "Engineering Mode · plots / modeling / simulation",
        "ja": "エンジニアリングモード · 作図／モデリング／シミュレーション",
        "ko": "엔지니어링 모드 · 도면 / 모델링 / 시뮬레이션",
        "fr": "Mode ingénierie · tracés / modélisation / simulation",
        "de": "Engineering-Modus · Diagramme / Modellierung / Simulation",
        "ru": "Инженерный режим · графики / моделирование / симуляция",
        "ar": "وضع الهندسة · رسوم / نمذجة / محاكاة",
        "es": "Modo ingeniería · gráficas / modelado / simulación",
        "pt": "Modo engenharia · gráficos / modelagem / simulação",
    },
    "home.shots.s4d": {
        "en": "Three tabs — engineering plots, math modeling, physics simulation — with one-click script or image export.",
        "ja": "エンジニアリング作図・数理モデリング・物理シミュレーションの 3 タブ。スクリプトや画像の書き出しも。",
        "ko": "엔지니어링 도면, 수학 모델링, 물리 시뮬레이션 3개 탭. 스크립트나 이미지로 내보낼 수 있습니다.",
        "fr": "Trois onglets — tracés d'ingénierie, modélisation mathématique, simulation physique — avec export du script ou de l'image.",
        "de": "Drei Tabs – technische Diagramme, mathematische Modellierung, physikalische Simulation – mit Skript- oder Bildexport.",
        "ru": "Три вкладки — инженерные графики, математическое моделирование, физическая симуляция — с экспортом скрипта или изображения.",
        "ar": "ثلاث تبويبات — رسوم هندسية، نمذجة رياضية، محاكاة فيزيائية — مع تصدير السكربت أو الصورة.",
        "es": "Tres pestañas —gráficas de ingeniería, modelado matemático y simulación física— con exportación de script o imagen.",
        "pt": "Três abas — gráficos de engenharia, modelagem matemática e simulação física — com exportação de script ou imagem.",
    },
    "home.shots.s5t": {
        "en": "Scheduled tasks · automation templates",
        "ja": "定期タスク · 自動化テンプレート",
        "ko": "예약 작업 · 자동화 템플릿",
        "fr": "Tâches planifiées · modèles d'automatisation",
        "de": "Geplante Aufgaben · Automatisierungsvorlagen",
        "ru": "Запланированные задачи · шаблоны автоматизации",
        "ar": "المهام المجدولة · قوالب الأتمتة",
        "es": "Tareas programadas · plantillas de automatización",
        "pt": "Tarefas agendadas · modelos de automação",
    },
    "home.shots.s5d": {
        "en": "Daily digest, weekly report and interview-prep templates work out of the box, scheduled entirely on your machine.",
        "ja": "日報・週報・面接対策リマインダーなどのテンプレートがすぐ使えます。スケジューリングは完全にローカル。",
        "ko": "일일 요약, 주간 보고서, 면접 준비 알림 등 템플릿을 바로 쓸 수 있고 예약은 전부 로컬에서 돌아갑니다.",
        "fr": "Synthèse quotidienne, rapport hebdomadaire, rappel de préparation d'entretien : prêts à l'emploi et planifiés en local.",
        "de": "Tagesdigest, Wochenbericht und Vorlagen zur Interviewvorbereitung sind sofort nutzbar – geplant wird rein lokal.",
        "ru": "Дайджест дня, недельный отчёт и напоминания о подготовке к собеседованию — готовы сразу, планировщик работает локально.",
        "ar": "ملخّص يومي وتقرير أسبوعي وتذكير بالتحضير للمقابلات، جاهزة فورًا والجدولة محلية بالكامل.",
        "es": "Resumen diario, informe semanal y recordatorio de preparación de entrevistas, listos para usar y programados en local.",
        "pt": "Resumo diário, relatório semanal e lembrete de preparação para entrevistas, prontos para usar e agendados localmente.",
    },
    "home.shots.s6t": {
        "en": "Task Center · cross-session progress board",
        "ja": "タスクセンター · セッション横断の進捗ボード",
        "ko": "작업 센터 · 세션 간 진행 보드",
        "fr": "Centre de tâches · suivi inter-sessions",
        "de": "Task-Center · Fortschrittsboard über Sitzungen hinweg",
        "ru": "Центр задач · доска прогресса между сессиями",
        "ar": "مركز المهام · لوحة تقدّم عابرة للجلسات",
        "es": "Centro de tareas · panel de avance entre sesiones",
        "pt": "Central de tarefas · painel de progresso entre sessões",
    },
    "home.shots.s6d": {
        "en": "Double-click a card to jump back into that session — the AI tracks every task across sessions.",
        "ja": "カードをダブルクリックで該当セッションへ復帰。AI はセッションをまたいで各タスクの進捗を把握します。",
        "ko": "카드를 더블클릭하면 해당 세션으로 돌아갑니다. AI는 세션을 넘나들며 각 작업의 진행 상황을 파악합니다.",
        "fr": "Double-cliquez une carte pour revenir à la session concernée : l'IA suit chaque tâche d'une session à l'autre.",
        "de": "Doppelklick auf eine Karte springt in die Sitzung – die KI verfolgt jede Aufgabe sitzungsübergreifend.",
        "ru": "Двойной клик по карточке возвращает в нужную сессию — ИИ отслеживает задачи во всех сессиях.",
        "ar": "انقر نقرًا مزدوجًا على البطاقة للعودة إلى جلستها، والذكاء الاصطناعي يتابع كل مهمة عبر الجلسات.",
        "es": "Haz doble clic en una tarjeta para volver a esa sesión: la IA sigue cada tarea entre sesiones.",
        "pt": "Dê um duplo clique no cartão para voltar à sessão: a IA acompanha cada tarefa entre sessões.",
    },
    "home.shots.s7t": {
        "en": "Industry scenario · trip budget analysis",
        "ja": "業界シナリオ · 旅行予算の分析",
        "ko": "산업 시나리오 · 여행 예산 분석",
        "fr": "Scénario métier · analyse de budget voyage",
        "de": "Branchenszenario · Reisebudget-Analyse",
        "ru": "Отраслевой сценарий · анализ бюджета поездки",
        "ar": "سيناريو قطاعي · تحليل ميزانية رحلة",
        "es": "Escenario sectorial · análisis de presupuesto de viaje",
        "pt": "Cenário setorial · análise de orçamento de viagem",
    },
    "home.shots.s7d": {
        "en": "Fuel, lodging and tickets itemized into price tables with sourcing notes.",
        "ja": "ガソリン代・宿泊・入場料を項目別に算出し、価格表と根拠を提示。",
        "ko": "기름값, 숙박, 입장료를 항목별로 계산하고 가격표와 근거를 함께 제시합니다.",
        "fr": "Carburant, hébergement et billets détaillés en tableaux de prix, sources à l'appui.",
        "de": "Kraftstoff, Unterkunft und Tickets als Preistabellen aufgeschlüsselt, mit Quellenangaben.",
        "ru": "Топливо, проживание и билеты разложены по таблицам цен с указанием источников.",
        "ar": "الوقود والإقامة والتذاكر مُفصّلة في جداول أسعار مع ذكر المصادر.",
        "es": "Combustible, alojamiento y entradas desglosados en tablas de precios con las fuentes.",
        "pt": "Combustível, hospedagem e ingressos detalhados em tabelas de preços com as fontes.",
    },
    "home.wf.shotcap": {
        "en": "The real canvas: drag nodes, tune parameters on the right, preview node by node",
        "ja": "実際のキャンバス：ノードをドラッグ、右側でパラメータ調整、ノードごとにプレビュー",
        "ko": "실제 캔버스: 노드를 끌고, 오른쪽에서 파라미터를 고치고, 노드별로 미리보기",
        "fr": "Le vrai canevas : glissez les nœuds, réglez les paramètres à droite, prévisualisez nœud par nœud",
        "de": "Der echte Canvas: Knoten ziehen, Parameter rechts anpassen, Knoten für Knoten ansehen",
        "ru": "Настоящий канвас: тащите узлы, меняйте параметры справа, смотрите каждый узел отдельно",
        "ar": "اللوحة الحقيقية: اسحب العقد، وعدّل المعطيات يمينًا، وعاين كل عقدة على حدة",
        "es": "El lienzo real: arrastra nodos, ajusta parámetros a la derecha y previsualiza nodo a nodo",
        "pt": "A tela real: arraste os nós, ajuste parâmetros à direita e veja nó por nó",
    },
}


def upsert(path, lang):
    s = io.open(path, encoding="utf-8").read()
    added, updated = 0, 0
    lines = []
    for k, tr in DATA.items():
        val = tr.get(lang)
        if not val:
            continue
        line = '  %s: %s,' % (json.dumps(k, ensure_ascii=False),
                              json.dumps(val, ensure_ascii=False))
        pat = re.compile(r'^\s*%s:.*$' % re.escape(json.dumps(k, ensure_ascii=False)), re.M)
        if pat.search(s):
            s = pat.sub(line, s)
            updated += 1
        else:
            lines.append(line)
            added += 1
    if lines:
        i = s.rfind("};")
        head, tail = s[:i].rstrip(), s[i:]
        if not head.endswith(","):
            head += ","
        s = head + "\n" + "\n".join(lines) + "\n" + tail
    io.open(path, "w", encoding="utf-8", newline="\n").write(s)
    return added, updated


if __name__ == "__main__":
    tot_a = tot_u = 0
    for lg in LANGS:
        f = "lang.%s.js" % lg
        if not os.path.exists(f):
            print("  ✗ 缺 %s" % f); continue
        a, u = upsert(f, lg)
        tot_a += a; tot_u += u
        print("  %-12s 新增 %2d · 更新 %2d" % (f, a, u))
    print("合计：新增 %d，更新 %d（%d key × %d 语言）" % (tot_a, tot_u, len(DATA), len(LANGS)))
