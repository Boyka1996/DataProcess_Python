package mask;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;

public class MaskRCNN {
	
	private String ip;//socket ip
	private int port;//socket port

	
	public MaskRCNN(String ip, int port) throws UnknownHostException, IOException{
		
        this.ip = ip;
        this.port = port;
		
	}
	
	public String detect(String imgSrc) throws IOException{
		Socket socket = new Socket(ip,port);
		 //获取输出流，向服务器端发送信息
		OutputStream os = socket.getOutputStream();//字节输出流
		PrintWriter pw = new PrintWriter(os);//将输出流包装为打印流
        
		InputStream is=socket.getInputStream();
		BufferedReader in = new BufferedReader(new InputStreamReader(is));//输出流
		pw.write(imgSrc);
        pw.flush();
        
        String info=null;
        String result = "";
        while((info=in.readLine())!=null){
        	System.out.println("我是客户端，Python服务器说："+info);
            result = result + info;
        }
        
        is.close();
        in.close();
        socket.close();
        return result;
	}	
}
