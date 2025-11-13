// Função para mostrar/ocultar as caixas de informação
function toggleBox(id) {
  // Oculta todas as caixas de informações
  document.querySelectorAll('.info-box').forEach(box => {
    box.style.display = 'none';
  });

  // Mostra a caixa correspondente ao botão clicado
  let box = document.getElementById(id);
  if (box) {
    box.style.display = 'block'; // Exibe a caixa
  }
}

// Atribui o evento de clique aos botões para mostrar as caixas de texto
document.getElementById("btn-control").onclick = function() {
  toggleBox('box-control');
};

document.getElementById("btn-key").onclick = function() {
  toggleBox('box-key');
};

document.getElementById("btn-trophy").onclick = function() {
  toggleBox('box-trophy');
};

document.addEventListener("click", function(event) {
if (!event.target.closest('.info-box') && !event.target.closest('.icon-buttons')) {
    document.querySelectorAll('.info-box').forEach(box => box.style.display = 'none');
}
});

// Abre/fecha a sidebar
document.getElementById("btn-menu").addEventListener("click", function() {
  let sidebar = document.getElementById("sidebar");
  if (sidebar.style.width === "250px") {
    sidebar.style.width = "0";
  } else {
    sidebar.style.width = "250px";
  }
});

// Mostra/esconde input
function toggleInput(id) {
  let input = document.getElementById(id);
  input.classList.toggle("show");
}

const btnMenu = document.getElementById('btn-menu');
const sidebar = document.getElementById('sidebar');

// Toggle sidebar open/close
btnMenu.addEventListener('click', () => {
  sidebar.classList.toggle('open');
});

// Função para esconder todas as info-box da sidebar
function hideSidebarBoxes() {
  document.querySelectorAll('.sidebar-info-box').forEach(box => {
    box.style.display = 'none';
  });
}

// Adiciona evento para todos os botões da sidebar
document.querySelectorAll('.sidebar-btn').forEach(button => {
  button.addEventListener('click', () => {
    hideSidebarBoxes();
    const boxId = button.getAttribute('data-box');
    const box = document.getElementById(boxId);
    if(box) {
      box.style.display = 'block';
    }
  });
});
// Função para abrir o e-mail de suporte
function openSupportEmail() {
  // Configure aqui o e-mail de suporte do seu jogo
  const supportEmail = 'suporte@mathgame.com';
  const subject = 'Suporte - Math Game - Relato de Problema';
  const body = `Olá equipe do Math Game,

Gostaria de relatar o seguinte problema:

[Descreva o problema aqui]

Informações adicionais:
- Dispositivo: 
- Navegador: 
- Fase em que ocorreu o problema: 

Atenciosamente,
[Seu Nome]`;

  // Codifica o assunto e corpo para URL
  const encodedSubject = encodeURIComponent(subject);
  const encodedBody = encodeURIComponent(body);
  
  // Abre o cliente de e-mail padrão
  window.location.href = `mailto:${supportEmail}?subject=${encodedSubject}&body=${encodedBody}`;
}

// Se você quiser também manter a função toggleInput para outros botões
function toggleInput(inputId) {
  // Sua lógica existente para toggleInput
  const input = document.getElementById(inputId);
  if (input) {
    input.style.display = input.style.display === 'none' ? 'block' : 'none';
  }
}
