(function(){
  var KEY='ipe_lang',LANGS=['en','ko','ja','zh-Hant','es','pt-BR','fr','de','id','th','vi','tr'];
  function toLang(tag){
    var t=String(tag||'').toLowerCase(),b=t.split('-')[0];
    if(b==='zh')return /(^|-)(tw|hk|mo|hant)(-|$)/.test(t)?'zh-Hant':null;
    if(b==='pt')return 'pt-BR';
    if(b==='in')return 'id';
    for(var i=0;i<LANGS.length;i++)if(LANGS[i].split('-')[0].toLowerCase()===b)return LANGS[i];
    return null;
  }
  function saved(){try{var v=localStorage.getItem(KEY);return LANGS.indexOf(v)>=0?v:null}catch(e){return null}}
  function save(l){try{localStorage.setItem(KEY,l)}catch(e){}}
  function target(stored,tags,alts){
    var l=stored;
    if(!l)for(var i=0;i<tags.length&&!l;i++)l=toLang(tags[i]);
    return l&&l!=='en'&&alts[l]?alts[l]:null;
  }
  if(document.documentElement.lang==='en'&&!/bot|crawl|spider|slurp|lighthouse/i.test(navigator.userAgent)){
    var alts={};
    [].forEach.call(document.querySelectorAll('link[rel="alternate"][hreflang]'),function(a){alts[a.hreflang]=a.getAttribute('href')});
    var href=target(saved(),navigator.languages||[navigator.language],alts);
    if(href)location.replace(href);
  }
  document.addEventListener('DOMContentLoaded',function(){
    var s=document.getElementById('lang-select');
    if(s)s.addEventListener('change',function(){save(s.options[s.selectedIndex].lang);location.href=s.value});
    var b=document.querySelector('.theme');if(!b)return;
    var root=document.documentElement;
    function dark(){var t=root.getAttribute('data-theme');return t?t==='dark':window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches}
    function label(){b.setAttribute('aria-label',dark()?b.dataset.light:b.dataset.dark)}
    b.addEventListener('click',function(){var n=dark()?'light':'dark';root.setAttribute('data-theme',n);try{localStorage.setItem('site-theme',n)}catch(e){}label()});
    label();
  });
})();
