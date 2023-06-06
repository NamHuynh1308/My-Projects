package webchatApplication;


public class ChatMessage {

	private String from;
	private String text;
	private String recipient;
	private String time;

	public ChatMessage() {
		super();
	}

	public ChatMessage(String from, String text, String recipient) {
		super();
		this.from = from;
		this.text = text;
		this.recipient = recipient;
		this.time = StringUtils.getCurrentTimeStamp();
	}

	public String getFrom() {
		return from;
	}

	public void setFrom(String from) {
		this.from = from;
	}

	public String getText() {
		return text;
	}

	public void setText(String text) {
		this.text = text;
	}

	public String getRecipient() {
		return recipient;
	}

	public void setRecipient(String recipient) {
		this.recipient = recipient;
	}
	
	public String getTime() {
		return time;
	}

	public void setTime() {
		this.recipient = StringUtils.getCurrentTimeStamp();
	}

}
