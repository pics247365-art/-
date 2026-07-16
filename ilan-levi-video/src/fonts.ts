import { continueRender, delayRender, staticFile } from "remotion";

export const FRANK_RUHL = "Frank Ruhl Libre";
export const ASSISTANT = "Assistant";
export const PLAYFAIR = "Playfair Display";

export const loadFonts = () => {
  const handle = delayRender("Loading fonts");

  const fonts = [
    new FontFace(FRANK_RUHL, `url(${staticFile("fonts/frank-ruhl-900.ttf")})`, {
      weight: "900",
      style: "normal",
    }),
    new FontFace(ASSISTANT, `url(${staticFile("fonts/assistant-300.ttf")})`, {
      weight: "300",
      style: "normal",
    }),
    new FontFace(ASSISTANT, `url(${staticFile("fonts/assistant-400.ttf")})`, {
      weight: "400",
      style: "normal",
    }),
    new FontFace(PLAYFAIR, `url(${staticFile("fonts/playfair-italic.ttf")})`, {
      weight: "400",
      style: "italic",
    }),
  ];

  Promise.all(fonts.map((f) => f.load())).then((loaded) => {
    loaded.forEach((f) => document.fonts.add(f));
    continueRender(handle);
  });
};
