import AccessEnum from "@/access/accessEnum";

/**
 * Check if the user has permission
 * @param loginUser Current login user
 * @param needAccess Required access
 * @return boolean Whether the user has permission
 */
import ACCESS_ENUM from "@/access/accessEnum";
const checkAccess = (loginUser: any, needAccess = ACCESS_ENUM.NOT_LOGIN) => {
  // Get the current login user's access (if there is no loginUser, it defaults to not logged in)
  const loginUserAccess = loginUser?.userRole ?? ACCESS_ENUM.NOT_LOGIN;
  if (needAccess === ACCESS_ENUM.NOT_LOGIN) {
    // No need to log in permission
    return true;
  }
  if (needAccess === ACCESS_ENUM.USER) {
    if (loginUserAccess === ACCESS_ENUM.NOT_LOGIN) {
      return false;
    }
  }
  if (needAccess === ACCESS_ENUM.ADMIN) {
    if (loginUserAccess === ACCESS_ENUM.ADMIN) {
      return true;
    }
  }
  return false;
};

export default checkAccess;
