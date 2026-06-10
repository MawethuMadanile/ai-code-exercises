class UserManager {
    private List<User> userList;
    private DBConn databaseConnection;

    public UserManager(DBConn databaseConnection) {
        this.databaseConnection = databaseConnection;
        this.userList = new ArrayList<>();
    }

    public boolean registerUser(String username, String password, String email) {
        if (!isValidInput(username, password, email)) return false;
        if (isUsernameTaken(username)) return false;

        User newUser = new User(username, password, email);
        userList.add(newUser);
        return databaseConnection.execute(
            "INSERT INTO users VALUES (?, ?, ?)", username, password, email
        );
    }

    public User findUserByUsername(String username) {
        for (User user : userList) {
            if (user.getUsername().equals(username)) return user;
        }
        return null;
    }

    private boolean isValidInput(String username, String password, String email) {
        return username.length() >= 3 && password.length() >= 8 && email.contains("@");
    }

    private boolean isUsernameTaken(String username) {
        return findUserByUsername(username) != null;
    }
}