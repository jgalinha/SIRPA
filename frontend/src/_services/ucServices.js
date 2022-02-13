import axios from "axios";

console.log("ucServices loaded");

const { REACT_APP_API_URL } = process.env;

const fetchUCs = async (authCtx) => {
  const config = {
    headers: {
      Accept: "application/json",
      Authorization: "Bearer " + authCtx.token,
    },
    mode: "cors",
  };
  const { data } = await axios.get(`${REACT_APP_API_URL}/uc/list`, config);
  return data;
};

const ucService = {
  fetchUCs,
};

export default ucService;
