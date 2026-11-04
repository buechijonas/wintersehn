const socialModules = import.meta.glob("./images/social/*.{svg,png}", {
  eager: true,
  import: "default",
});

export const social = Object.fromEntries(
  Object.entries(socialModules).map(([path, src]) => [
    path.split("/").pop().replace(/\.(svg|png)$/, ""),
    src,
  ]),
);
