
        // Elementos do DOM
        const startBtn = document.getElementById('startBtn');
        const configBtn = document.getElementById('configBtn');
        const exitBtn = document.getElementById('exitBtn');
        const configModal = document.getElementById('configModal');
        const closeBtn = document.querySelector('.close-btn');
        const saveConfigBtn = document.getElementById('saveConfig');
        const userAvatar = document.getElementById('userAvatar');
        const userName = document.getElementById('userName');

        // Simulação de dados do usuário (normalmente viriam do backend)
        const userData = {
            name: "Matemático123",
            avatar: "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='60' height='60' viewBox='0 0 60 60'><circle cx='30' cy='30' r='30' fill='%234a7c59'/><circle cx='30' cy='20' r='10' fill='%23ffcc00'/><path d='M30 40 Q40 55 20 55 Q30 45 30 40' fill='%23ffcc00'/></svg>"
        };

        // Detectar orientação da tela
        function checkOrientation() {
            if (window.innerHeight > window.innerWidth) {
                console.log("Modo retrato detectado");
                // Em dispositivos móveis, você pode forçar a orientação paisagem
                // Nota: Isso só funciona em alguns navegadores e geralmente requer interação do usuário
            } else {
                console.log("Modo paisagem detectado");
            }
        }

        // Verificar orientação ao carregar e redimensionar
        window.addEventListener('load', checkOrientation);
        window.addEventListener('resize', checkOrientation);
        window.addEventListener('orientationchange', checkOrientation);

        // Carregar dados do usuário
        function loadUserData() {
            userName.textContent = userData.name;
            userAvatar.src = userData.avatar;
        }

        // Event Listeners
        startBtn.addEventListener('click', function() {
            alert('Iniciando o jogo...');
            // Aqui você redirecionaria para a tela do jogo
            // window.location.href = 'game.html';
        });

        configBtn.addEventListener('click', function() {
            configModal.style.display = 'flex';
        });

        exitBtn.addEventListener('click', function() {
            if(confirm('Tem certeza que deseja sair do jogo?')) {
                // Salvar progresso antes de sair
                saveProgress();
                // Fechar o jogo
                if (navigator.app) {
                    navigator.app.exitApp();
                } else if (navigator.device) {
                    navigator.device.exitApp();
                } else {
                    window.close();
                }
            }
        });

        closeBtn.addEventListener('click', function() {
            configModal.style.display = 'none';
        });

        saveConfigBtn.addEventListener('click', function() {
            const joystickSize = document.getElementById('joystickSize').value;
            const captionSize = document.getElementById('captionSize').value;
            const language = document.getElementById('language').value;
            
            // Salvar configurações (normalmente em localStorage ou backend)
            localStorage.setItem('joystickSize', joystickSize);
            localStorage.setItem('captionSize', captionSize);
            localStorage.setItem('language', language);
            
            alert('Configurações salvas com sucesso!');
            configModal.style.display = 'none';
        });

        // Fechar modal ao clicar fora dele
        window.addEventListener('click', function(event) {
            if (event.target === configModal) {
                configModal.style.display = 'none';
            }
        });

        // Salvar progresso do jogador
        function saveProgress() {
            const progress = {
                level: 1,
                score: 0,
                completedChallenges: []
            };
            localStorage.setItem('gameProgress', JSON.stringify(progress));
            console.log('Progresso salvo!');
        }

        // Carregar configurações salvas
        function loadSettings() {
            const savedJoystickSize = localStorage.getItem('joystickSize');
            const savedCaptionSize = localStorage.getItem('captionSize');
            const savedLanguage = localStorage.getItem('language');
            
            if(savedJoystickSize) {
                document.getElementById('joystickSize').value = savedJoystickSize;
            }
            
            if(savedCaptionSize) {
                document.getElementById('captionSize').value = savedCaptionSize;
            }
            
            if(savedLanguage) {
                document.getElementById('language').value = savedLanguage;
            }
        }

        // Inicialização
        document.addEventListener('DOMContentLoaded', function() {
            loadUserData();
            loadSettings();
            checkOrientation();
        });
        // === PERSONALIZAÇÃO DO AVATAR ===
const avatarInput = document.getElementById('avatarInput');

// Clicar no avatar abre o seletor de imagem
userAvatar.addEventListener('click', () => {
    // Em dispositivos móveis, isso abre a galeria ou câmera
    avatarInput.click();
});

// Quando o usuário escolhe uma imagem
avatarInput.addEventListener('change', function() {
    const file = this.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(event) {
        const newAvatar = event.target.result;
        userAvatar.src = newAvatar;

        // Salva no localStorage
        try {
            localStorage.setItem('userAvatar', newAvatar);
            console.log('Avatar salvo com sucesso.');
        } catch (e) {
            console.warn('Erro ao salvar avatar (talvez o arquivo seja grande demais)', e);
        }
    };
    reader.readAsDataURL(file);
});

// Carregar avatar salvo (ou padrão)
function loadUserAvatar() {
    const savedAvatar = localStorage.getItem('userAvatar');
    if (savedAvatar) {
        userAvatar.src = savedAvatar;
    } else {
        userAvatar.src = userData.avatar;
    }
}

// Chame dentro do DOMContentLoaded:
document.addEventListener('DOMContentLoaded', function() {
    loadUserData();
    loadUserAvatar(); // 👈 importante
    loadSettings();
    checkOrientation();
});
