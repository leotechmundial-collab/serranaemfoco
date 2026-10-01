(() => {
  const gate = document.getElementById('entrada');
  const button = document.getElementById('entrar');
  const status = document.getElementById('entrada-status');
  const frame = document.getElementById('video-player');
  let player;
  let unavailable = false;
  let attempted = false;
  let playbackTimer;
  const openSite = () => {
    clearTimeout(playbackTimer);
    gate.hidden = true;
    document.getElementById('site-content').inert = false;
    document.body.classList.remove('entrada-aberta');
    document.querySelector('.brand').setAttribute('tabindex', '-1');
    document.querySelector('.brand').focus();
  };
  const fail = () => {
    unavailable = true;
    button.disabled = false;
    button.textContent = 'Veja antes que saia do ar';
    status.textContent = 'O YouTube não carregou o vídeo. Use o botão para entrar no site.';
  };
  const loadTimer = setTimeout(fail, 15000);
  const url = new URL(frame.dataset.src);
  url.searchParams.set('enablejsapi', '1');
  url.searchParams.set('origin', location.origin);
  frame.src = url.href;
  window.onYouTubeIframeAPIReady = () => {
    player = new YT.Player('video-player', {
      events: {
        onReady: () => {
          clearTimeout(loadTimer);
          unavailable = false;
          button.disabled = false;
          button.textContent = 'Veja antes que saia do ar';
          status.textContent = 'Ao entrar, o vídeo começa com som.';
        },
        onStateChange: (event) => {
          if (attempted && event.data === YT.PlayerState.PLAYING) openSite();
        },
        onAutoplayBlocked: () => {
          clearTimeout(playbackTimer);
          status.textContent = 'O navegador bloqueou a reprodução. Toque novamente para iniciar com som.';
          button.disabled = false;
        },
        onError: () => { clearTimeout(loadTimer); fail(); }
      }
    });
  };
  button.addEventListener('click', () => {
    if (unavailable) { openSite(); return; }
    if (!player || typeof player.playVideo !== 'function') return;
    attempted = true;
    player.unMute();
    player.setVolume(100);
    player.playVideo();
    status.textContent = 'Iniciando o vídeo com som…';
    clearTimeout(playbackTimer);
    playbackTimer = setTimeout(() => {
      openSite();
    }, 7000);
  });

  const api = document.createElement('script');
  api.src = 'https://www.youtube.com/iframe_api';
  api.onerror = () => { clearTimeout(loadTimer); fail(); };
  document.head.appendChild(api);
})();
