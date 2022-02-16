const randomColor = () => {
  const random = Math.floor(Math.random() * 16777215).toString(16);
  const color = "#" + random;
  return color;
};

const objToBodyObj = (obj) => {
  var str = "";
  for (var key in obj) {
    if (str !== "") {
      str += "&";
    }
    str += key + "=" + encodeURIComponent(obj[key]);
  }
  return str;
};

const Utils = {
  randomColor,
  objToBodyObj,
};

export default Utils;
