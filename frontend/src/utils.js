const randomColor = () => {
  const random = Math.floor(Math.random() * 16777215).toString(16);
  const color = "#" + random;
  return color;
};

const Utils = {
  randomColor,
};

export default Utils;
