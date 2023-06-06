package webchatApplication;

import java.security.Principal;
public class User implements Principal {
 
    String name;
 
    public User(String name) {
        this.name = name;
    }
 
    public String getName() {
        return name;
    }
}
