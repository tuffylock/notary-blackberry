# notary-blackberry

clicking is hard

[homepage](http://www.tuffylock.fyi/notary-blackberry/)


bookmarklet code (draggable/clickable link on homepage^. github strips the js from the link):

```
javascript:(function(){
  blackberryJS=document.createElement('SCRIPT');
  blackberryJS.type='text/javascript';
  blackberryJS.src='http://tuffylock.github.io/notary-blackberry/bookmarklet.js?v='+parseInt(Math.random()*99999999);
  document.getElementsByTagName('head')[0].appendChild(blackberryJS);
})();
```
