const socialModules = import.meta.glob("./images/social/*.svg", {
  eager: true,
  import: "default",
});

export const social = Object.fromEntries(
  Object.entries(socialModules).map(([path, src]) => [
    path.split("/").pop().replace(".svg", ""),
    src,
  ]),
);
