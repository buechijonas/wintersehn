export { profiles } from "./profiles.js";
export { social } from "./social.js";

const undrawModules = import.meta.glob("./images/undraws/*.svg", {
  eager: true,
  import: "default",
});
const flatModules = import.meta.glob("./images/flats/**/*.svg", {
  eager: true,
  import: "default",
});
const countryModules = import.meta.glob("./images/countries/*.svg", {
  eager: true,
  import: "default",
});

export const undraws = Object.fromEntries(
  Object.entries(undrawModules).map(([path, src]) => [
    path.split("/").pop().replace(".svg", ""),
    src,
  ]),
);

const flatEntries = Object.entries(flatModules).map(([path, src]) => {
  const segments = path
    .replace("./images/flats/", "")
    .replace(".svg", "")
    .split("/");
  return {
    key: segments.join("/"),
    folder: segments.length > 1 ? segments[0] : null,
    src,
  };
});

export const flats = Object.fromEntries(
  flatEntries.map(({ key, src }) => [key, src]),
);

export const flatCategories = flatEntries.reduce(
  (categories, { key, folder }) => {
    if (!folder) return categories;
    categories[folder] ??= [];
    categories[folder].push(key);
    return categories;
  },
  {},
);

export const countries = Object.fromEntries(
  Object.entries(countryModules).map(([path, src]) => [
    path.split("/").pop().replace(".svg", ""),
    src,
  ]),
);
