import axios from "axios";
import Utils from "../utils";

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
  setter = () => {},
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
        return response.json();
      })
      .then((data) => {
        setter(data);
      });
  } catch (error) {}
};

const crudService = {
  fetchAPI,
  postAPI,
};

export default crudService;
