import jwt_decode from "jwt-decode";

console.log("userServices loaded");

const { REACT_APP_API_URL } = process.env;

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

const user_login = async (body, setIsLoading, authCtx) => {
  try {
    let response = await fetch(`${REACT_APP_API_URL}/auth/login`, {
      method: "POST",
      body: objToBodyObj(body),
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Accept: "Set-Cookie",
      },
      mode: "cors",
    });
    if (response.ok) {
      setIsLoading(false);
      const data = await response.json();
      const tokenData = jwt_decode(data.access_token);
      authCtx.login(data.access_token, {
        email: tokenData.sub,
        id: tokenData.id,
        username: tokenData.username,
        exp: tokenData.exp,
        nbf: tokenData.nbf,
        isTeacher: tokenData.isTeacher,
        isStudent: tokenData.isStudent,
        isSuper: tokenData.isSuper,
      });
      return true;
    } else {
      throw Error;
    }
  } catch (error) {
    setIsLoading(false);
    console.log("Authentication failed" + error);
    alert("Authentication failed!");
  }
};

const userService = {
  user_login,
};

export default userService;
