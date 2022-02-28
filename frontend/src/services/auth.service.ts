import axios from "axios";
const API_URL = import.meta.env.VITE_API_URL;
console.log(import.meta.env);

class AuthService {
  login(user: any) {
    return axios
      .post(API_URL + "/auth", {
        username: user.username,
        password: user.password,
      })
      .then((response) => {
        if (response.data.data.token) {
          localStorage.setItem("user", JSON.stringify(response.data.data));
        }
        return response.data;
      });
  }
  logout() {
    localStorage.removeItem("user");
  }
  register(user: any) {
    return axios.post(API_URL + "/auth" + "/register", {
      username: user.username,
      password: user.password,
    });
  }
}
export default new AuthService();
