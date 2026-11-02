# How the 3D is drawn

Everything is vector geometry; nothing needs JavaScript or WebGL.

## Isometric pillar — `pillar(cx, cy, s, h, color)`
An isometric box shows three faces. With base-diamond centre `(cx, cy)` and half-width `s`:
```
top   : (cx, cy-s/2-h) (cx+s, cy-h) (cx, cy+s/2-h) (cx-s, cy-h)
left  : (cx-s, cy-h) (cx, cy+s/2-h) (cx, cy+s/2) (cx-s, cy)
right : (cx, cy+s/2-h) (cx+s, cy-h) (cx+s, cy) (cx, cy+s/2)
```
Light direction is faked with `shade()`: top x1.35 (lighter), left x1.0, right x0.62 (darker). A thin white
polyline along the top edges adds a highlight so the edges read as bevels.

## Text lying on a face — `top_label()`
The label is placed with `matrix(0.866 0.5 -0.866 0.5 0 0)`: the text's x-axis maps to the face's down-right edge
(30 degrees) and its y-axis to the down-left edge, so words sit flat on the top plane.

## Extruded titles — `extruded()`
The same string is drawn `depth` times, each copy offset 1 px down-right and darkened toward the back; the bright
face copy is drawn last. Seen from the front this reads as solid thickness (the 12-layer hero name, 6-layer headers).

## Pedestals — `pedestal()`
Cylinder = side path (rect with an elliptical bottom edge) + top ellipse + inner dashed ring (`.ring`, animated
`stroke-dashoffset`) + radial glow. A blurred black ellipse underneath is the contact shadow.

## Perspective floor — `floor()`
Vertical lines converge on a vanishing point at the horizon; horizontal lines are spaced with `(k/9)^2.1` so rows
get farther apart toward the viewer. A clipPath keeps the grid inside the rounded card.

## Depth cues
* Soft shadows (`feGaussianBlur`) under every object.
* Embers drawn on top of scenery but under UI text for layering.
* Characters bob at different speeds (`.bob`, `.bob2`, `.bob3`) so motion feels parallax-like.

## Limits
* No real camera rotation, no mouse interaction: GitHub strips scripts.
* Browsers differ slightly in SVG animation smoothness; all animations loop and degrade to a static image.
