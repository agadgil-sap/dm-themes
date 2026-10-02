"""Build the three website variations from shared, authored components."""
from pathlib import Path

source = Path(__file__).resolve().parent
root = source.parent
styles = ['tokens.css', 'components.css', 'themes.css', 'responsive.css']
scripts = ['data.js', 'components.js', 'pages.js', 'forms.js', 'app.js']
css = '\n'.join((source / 'css' / name).read_text() for name in styles)
js = '\n'.join((source / 'js' / name).read_text() for name in scripts)
shell = (source / 'shell.html').read_text()
result = shell.replace('/* SITE_STYLES */', css).replace('/* SITE_SCRIPTS */', js)
assert chr(0x2014) not in result
for name in ['index.html', 'dental-match-website.html', 'dental-match-ab-refinements.html']:
    (root / name).write_text(result)
(root / '.lavish' / 'dental-match-website-preview.html').write_text(result)
print('Built three website variations, the existing page alias and the Lavish preview.')
