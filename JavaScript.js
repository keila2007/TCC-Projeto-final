// Função para mostrar/ocultar as caixas de informação
function toggleBox(id) {
  // Oculta todas as caixas de informações
  document.querySelectorAll('.info-box').forEach(box => {
    box.style.display = 'none';
  });

  // Mostra a caixa correspondente ao botão clicado
  let box = document.getElementById(id);
  if (box) {
    box.style.display = 'block';
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

// Fecha as caixas ao clicar fora
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

// Fecha sidebar ao clicar fora
document.addEventListener('click', function(event) {
  const sidebar = document.getElementById('sidebar');
  const hamburger = document.getElementById('btn-menu');
  
  if (!sidebar.contains(event.target) && !hamburger.contains(event.target) && sidebar.style.width === "250px") {
    sidebar.style.width = "0";
  }
});

// Mostra/esconde input
function toggleInput(id) {
  let input = document.getElementById(id);
  if (input) {
    input.classList.toggle("show");
  }
}

// Função para abrir o e-mail de suporte
function openSupportEmail() {
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

  const encodedSubject = encodeURIComponent(subject);
  const encodedBody = encodeURIComponent(body);
  
  window.location.href = `mailto:${supportEmail}?subject=${encodedSubject}&body=${encodedBody}`;
}

// Fecha sidebar ao redimensionar a janela (para mobile)
window.addEventListener('resize', function() {
  const sidebar = document.getElementById('sidebar');
  if (window.innerWidth > 768 && sidebar.style.width === "250px") {
    sidebar.style.width = "0";
  }
});
