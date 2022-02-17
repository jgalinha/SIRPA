import axios from "axios";

console.log("crudServices loaded");

const { REACT_APP_API_URL } = process.env;

const fetchAPI = async (authCtx, endPoint) => {
  const config = {
    headers: {
      Accept: "application/json",
      Authorization: "Bearer " + authCtx.token,
    },
    mode: "cors",
  };
  const { data } = await axios
    .get(`${REACT_APP_API_URL}${endPoint}`, config)
    .then()
    .catch((error) => {
      // console.log(error.response.data);
      // console.log(error.response.status);
      // console.log(error.response.headers);
      return Promise.reject(error);
    });
  return data;
};

const postAPI = async (
  authCtx,
  endPoint,
  body,
  setter,
  setError,
  config = {}
) => {
  try {
    const data = await fetch(`${REACT_APP_API_URL}${endPoint}`, {
      method: "POST",
      body: JSON.stringify(body),
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        Authorization: "Bearer " + authCtx.token,
      },
      mode: "cors",
    })
      .then((response) => {
        if (!response.ok) {
          return Promise.reject(response);
        }
        return response.json();
      })
      .then((data) => {
        setter(data);
        return data;
      })
      .catch((error) => {
        if (error.text) {
          error.text().then((error_msg) => {
            const obj = JSON.parse(error_msg);
            const msg = obj.detail.error.error_detail;
            setError({ ...obj.detail.error });
          });
        }
      });
    return data;
  } catch (e) {
    console.log(e);
  }
};

const crudService = {
  fetchAPI,
  postAPI,
};

export default crudService;
