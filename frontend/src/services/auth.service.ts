import axios from "axios";
const API_URL = "http://localhost:5000/auth/";

class AuthService {
  login(user: any) {
    return axios
      .post(API_URL, {
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
    return axios.post(API_URL + "register", {
      username: user.username,
      password: user.password,
    });
  }
}
export default new AuthService();
