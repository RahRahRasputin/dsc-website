// katex-render.js — renders $...$ formulas using KaTeX
// Called after katex.min.js has loaded (via defer)
(function() {
  // Wait for katex to be available
  function tryRender() {
    if (typeof katex === 'undefined') {
      setTimeout(tryRender, 300);
      return;
    }
    renderAll();
  }

  function renderAll() {
    // Walk all text nodes looking for $...$
    walk(document.body);

    function walk(node) {
      if (node.nodeType === 3) { // TEXT node
        var text = node.textContent;
        if (text.indexOf('$') < 0) return;

        var parts = [];
        var last = 0;
        var inMath = false;
        var start = -1;

        for (var i = 0; i < text.length; i++) {
          var c = text.charAt(i);
          if (c === '$') {
            if (!inMath) {
              // Opening $
              // Check it's not $$ (display math)
              if (i + 1 < text.length && text.charAt(i + 1) === '$') {
                // $$ — skip for now, handle display math separately
                i++; // skip second $
                continue;
              }
              inMath = true;
              start = i;
            } else {
              // Closing $
              inMath = false;
              var expr = text.substring(start + 1, i);
              if (expr.length > 0) {
                try {
                  var rendered = katex.renderToString(expr, {
                    displayMode: false,
                    throwOnError: false
                  });
                  parts.push({type: 'html', html: rendered});
                } catch(e) {
                  parts.push({type: 'text', text: text.substring(start, i + 1)});
                }
              } else {
                parts.push({type: 'text', text: '$'});
              }
              last = i + 1;
            }
          }
        }

        if (parts.length > 0) {
          // Rebuild the text node's parent with rendered content
          var parent = node.parentNode;
          var fragment = document.createDocumentFragment();
          var cursor = 0;
          for (var pi = 0; pi < parts.length; pi++) {
            var part = parts[pi];
            // Add text before this part
            if (part.type === 'html') {
              // Parse HTML fragment
              var temp = document.createElement('span');
              temp.innerHTML = part.html;
              while (temp.firstChild) {
                fragment.appendChild(temp.firstChild);
              }
            } else {
              fragment.appendChild(document.createTextNode(part.text));
            }
          }
          parent.replaceChild(fragment, node);
        }
        return;
      }

      if (node.nodeType === 1) { // ELEMENT node
        // Don't enter script, style, or SVG elements
        var tag = node.tagName.toLowerCase();
        if (tag === 'script' || tag === 'style' || tag === 'math' || tag === 'svg') return;
        // Don't process already-rendered KaTeX
        if (node.classList && node.classList.contains('katex')) return;
        for (var child = node.firstChild; child; child = child.nextSibling) {
          walk(child);
        }
      }
    }
  }

  tryRender();
})();