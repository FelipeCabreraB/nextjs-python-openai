import Cookie from "js-cookie";
import { v4 as uuidv4 } from "uuid";

export const setCookie = () => {
  if (!Cookie.get("session_id")) {
    Cookie.set("session_id", uuidv4(), { expires: 2 });
  }
};
