# Objects: showing the subject's things without photos

When a page needs the subject's objects (the breads, the jars, the tools, the product) and there
are no photos, generated pages draw them as plain shapes: a CSS circle for a loaf, a rounded
rectangle for a phone, one grey low-poly prism for a rock. These read as placeholders, and they
pull the whole page down to wireframe level. A designer either gets a real image, makes the object
properly, or shows something else.

## The ladder

Take the first rung that is available and good enough:

1. **Real photos** of this business's things (the user's assets, the project's images). Ask for them
   when they would carry the page and nothing is there.
2. **Openly licensed photos or models** of the exact thing, when the license allows it and the
   source is reliable: Poly Haven (CC0 models, HDRIs and textures, `https://api.polyhaven.com`, sends a
   `User-Agent`), ambientCG (CC0 materials, `https://ambientcg.com/api/v3/assets`), Wikimedia Commons
   with its stated license and credit. Never hotlink random stock URLs.
3. **A made 3D object rendered to a still image.** Build the object procedurally in three.js with the
   recipes in the `cinematic` skill's `references/modelling.md`, light it properly, render it once in
   the browser (Playwright) on the exact background color of the section it will sit on, and ship
   the screenshot as WebP or PNG with `width`, `height` and `alt`. This gives a product-shot or
   clay-render look with no runtime cost, which is what most ordinary pages need. Keep the scene
   file in the scratch directory, or in the project only when the user wants to re-render it.
4. **A live 3D object**, only when interaction is the point (turn it, configure it, take it apart):
   a small three.js canvas that renders on demand, with the still from rung 3 as its poster and
   fallback. For a whole scroll-driven scene, that's the `cinematic` skill.
5. **A crafted illustration in SVG**, built in layers, never one flat fill:
   - the silhouette from real proportions (measure a reference photo or drawing; trace its
     characteristic outline as exact curves, not a primitive);
   - a base gradient for the form, a form-shadow gradient on the side away from the light, a rim
     highlight on the edge toward it, all from one light direction shared with the page's shadows;
   - texture from the material: `feTurbulence` into `feDiffuseLighting` or `feSpecularLighting` as a
     bump map (crust, stone, paper, fabric), with `color-interpolation-filters="sRGB"`;
   - the functional details that make it that object (the score on a loaf, the thread on a lid, the
     bolt hole in a hold, the stitching on a cover);
   - a soft cast shadow (a blurred ellipse) so it stands on the page.
   A flat, graphic style is fine when it is the concept (a pictogram system, a linocut look), but
   then it is drawn to the same rules: exact geometry, consistent stroke and corner, detail.
6. **Type or the graphic device beside the object**: the names of the breads set large, the jar's
   label as the hero. This carries the objects the page doesn't show; it doesn't replace all of
   them. When the subject is physical things (food, products, tools, a place) and rungs 1 and 2 are
   empty, at least one object is made on rung 3, 4 or 5 and leads a view. A page about honey with
   no jar, comb or candle anywhere reads as a poster for a brand nobody has seen.
7. **Leave it out**, only for an object that failed the craft bar twice, and say which images
   would help most.

CSS 3D (`transform-style: preserve-3d`) works for boxy objects only (a book, a box, a card, a phone):
shade each face from one lightness token (top lightest, front middle, side darkest). Never build
organic objects from CSS shapes.

## The craft bar

Before an object goes on the page, check it at the size it will be shown:

- **Silhouette**: would someone name the object from its outline alone?
- **Form**: is it lit from one direction, with a light side, a shadow side and an edge highlight?
  Are edges bevelled or rounded the way the real thing is, not razor sharp?
- **Material**: does the surface say what it is made of (rough, glossy, translucent, fibrous)?
- **Detail**: does it have the two or three details that make it this object and not the category?
- **Grounding**: does it sit on something (a contact shadow, a surface, a plinth), or float?
- **Set**: do several objects share one light, one camera angle and one finish?

If an object fails two of these, fix what failed (usually the light direction, the detail or the
grounding) and check it again. Take a lower rung only when the second attempt fails too.
