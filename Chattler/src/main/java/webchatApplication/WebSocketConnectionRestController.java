package webchatApplication;


import java.util.Set;
import java.io.File;
import java.io.IOException;
import java.io.FileWriter;
import java.io.BufferedWriter;
import java.util.HashMap;
import javax.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.Scanner;
 
@RestController
public class WebSocketConnectionRestController{
    
    @Autowired
    private ActiveUserManager activeSessionManager;
    private HashMap<String, String> userPassCombos;
    private File userFile = new File(System.getProperty("user.dir") + "/src/main/resources/static/users.txt");
    private String recentUser;
    private String nextUser;
    
    @PostMapping("/rest/user-connect")
    public String userConnect(HttpServletRequest request) {
        String remoteAddr = "";
        if (request != null) {
            remoteAddr = request.getHeader("Remote_Addr");
            if (StringUtils.isEmpty(remoteAddr)) {
                remoteAddr = request.getHeader("X-FORWARDED-FOR");
                if (remoteAddr == null || "".equals(remoteAddr)) {
                    remoteAddr = request.getRemoteAddr();
                }
            }
        }
        
        activeSessionManager.add(nextUser, remoteAddr);
        recentUser = nextUser;
        nextUser = "";
        return remoteAddr;
    }
    
    @PostMapping("/rest/set-next")
    public void setNext(@ModelAttribute("username") String next) {
    	nextUser = next;
    }
    
    @PostMapping("/rest/user-disconnect")
    public String userDisconnect(@ModelAttribute("username") String userName) {
        activeSessionManager.remove(userName);
        return "disconnected";
    }
    
    @PostMapping("/rest/user-verify")
    public String userVerify(HttpServletRequest request, @ModelAttribute("username") String userName, @ModelAttribute("password") String password) throws IOException {
    	readUsersFile();
    	if (userPassCombos.isEmpty()) return "false";
    	else if (!userPassCombos.containsKey(userName.toLowerCase()) || !(userPassCombos.get(userName.toLowerCase()).equals(password))) return "false";
    	else return "true";
    }
    
    @GetMapping("/rest/check-name")
    public String checkName(HttpServletRequest request, @ModelAttribute("username") String userName) throws IOException{
    	readUsersFile();
    	if (userPassCombos.isEmpty()) return "true";
    	else if (userPassCombos.containsKey(userName.toLowerCase())) return "false";
    	else return "true";
    }
    
    @GetMapping("/rest/create-user")
    public String createUser(HttpServletRequest request, @ModelAttribute("username") String userName, @ModelAttribute("password") String passWord) throws IOException {
    	FileWriter fileWriter = new FileWriter(userFile, true);
    	BufferedWriter writer = new BufferedWriter(fileWriter);
    	try {
    			writer.write("{" + userName.toLowerCase() + ", " + passWord + "}\n");
    			writer.close();
    			readUsersFile();
    			return "Created account! Redirecting to Log-In page.";
    	}
    	catch (Exception e) {return "Could not make account, redirecting to log-in page.";}
    }
    
    @GetMapping("/rest/get-recent-user")
    public String getRecentUser() {
    	return recentUser;
    }
    @GetMapping("/rest/get-next")
    public String getNext() {
    	return nextUser;
    }
    @GetMapping("/rest/active-users-except/{userName}")
    public String[] getActiveUsersExceptCurrentUser(@PathVariable String userName) {
    	String[] returnArray = new String[activeSessionManager.getActiveUsersExceptCurrentUser(userName).size()];
    	for (int i = 0; i < returnArray.length; ++i) {
    		returnArray[i] = activeSessionManager.getActiveUsersExceptCurrentUser(userName).toArray()[i].toString();
    	}
        return returnArray;
    }
    @GetMapping("/rest/amount-active-users-except/{userName}")
    public int getAmountActiveUsersExceptCurrentUser(@PathVariable String userName) {
        return activeSessionManager.getActiveUsersExceptCurrentUser(userName).size();
    }
    
    private void readUsersFile() throws IOException {
    	userPassCombos = new HashMap<String, String>();
    	Scanner scanner = new Scanner(userFile);
    	String next = "";
    	String[] nextSplit;
    	while (scanner.hasNextLine()) {
    		next = scanner.nextLine();
    		nextSplit = next.split(", ", 2);
    		nextSplit[0] = nextSplit[0].substring(1);
    		nextSplit[1] = nextSplit[1].substring(0, nextSplit[1].length() - 1);
    		userPassCombos.put(nextSplit[0].toLowerCase(), nextSplit[1]);
    	}
    	scanner.close();
    }
}
