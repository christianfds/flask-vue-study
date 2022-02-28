import type { AxiosRequestHeaders } from "axios";

export default function authHeader() {
  const user = JSON.parse(localStorage.getItem("user") as string);
  let header: AxiosRequestHeaders;
  if (user && user.token) {
    header = { Authorization: "Bearer " + user.token };
  } else {
    header = {};
  }
  return header;
}
