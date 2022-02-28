import axios from "axios";
import authHeader from "./auth-header";
const API_URL = "http://localhost:5000";
class UserService {
  approvePending(photo_id: string) {
    return axios.post(
      API_URL + "/photos/pending/" + photo_id,
      { status: "accepted" },
      { headers: authHeader() }
    );
  }
  denyPending(photo_id: string) {
    return axios.post(
      API_URL + "/photos/pending/" + photo_id,
      { status: "rejected" },
      { headers: authHeader() }
    );
  }
  addComment(photo_id: string, message: string) {
    return axios.post(
      API_URL + "/photos/" + photo_id + "/comment",
      { message: message },
      { headers: authHeader() }
    );
  }
  reactToPost(photo_id: string) {
    return axios.post(
      API_URL + "/photos/" + photo_id + "/react",
      {},
      { headers: authHeader() }
    );
  }
  unreactToPost(photo_id: string) {
    return axios.delete(API_URL + "/photos/" + photo_id + "/react", {
      headers: authHeader(),
    });
  }
  getApprovedPosts() {
    return axios.get(API_URL + "/photos", { headers: authHeader() });
  }
  getPendingPosts() {
    return axios.get(API_URL + "/photos/pending", { headers: authHeader() });
  }
  postImage(data: any) {
    return axios.post(API_URL + "/photos", data, { headers: authHeader() });
  }
}
export default new UserService();
