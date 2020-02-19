package mask;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.dom4j.Document;
import org.dom4j.DocumentException;
import org.dom4j.Element;
import org.dom4j.io.SAXReader;
import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.imgcodecs.Imgcodecs;

import com.alibaba.fastjson.JSONObject;

import JsonBean.CoCo_Annotation;
import JsonBean.CoCoCategory;
import JsonBean.CoCo_Image;
import JsonBean.CoCo_Inastance;
import JsonBean.CoCo_Info;
import JsonBean.CoCoLicense;

public class XmlToMaskJson {
	
	public static void main(String ars[]) throws DocumentException, IOException {
		String srcLabelsPath = "/media/chase/A/新安全帽/鲁能总标注/xidai/Annotations/";
		String dst = "/media/chase/A/新安全帽/鲁能总标注/bushing.json";
		String imageSrc = "/media/chase/毛衣爱学习/workspace/images/";
		File file = new File(srcLabelsPath);
		File[] files = file.listFiles();
		
		CoCo_Info info = new CoCo_Info();//info
		List<CoCoLicense> licenses = new ArrayList<>();//licenses
		List<CoCo_Image> images = new ArrayList<>();//images
		List<CoCo_Annotation> annotations = new ArrayList<>();//annotations
		List<CoCoCategory> categories = new ArrayList<>();//categories
		String type = "instances";//type
		
		licenses.add(new CoCoLicense("", 1, ""));		
		/*categories.add(new CoCoCategory("bluehat", 1, "bluehat"));
		categories.add(new CoCoCategory("redhat", 2, "redhat"));
		categories.add(new CoCoCategory("yellowhat", 3, "yellowhat"));
		categories.add(new CoCoCategory("whitehat", 4, "whitehat"));
		categories.add(new CoCoCategory("orangehat", 5, "orangehat"));*/
		categories.add(new CoCoCategory("bushing", 1, "bushing"));
		//categories.add(new CoCoCategory("Oil pollution", 1, "Oil pollution"));
		//categories.add(new CoCoCategory("damaged", 2, "damaged"));
		int image_id=1;
		int ann_id =1;
		
        for (File f:files) {
			System.out.println(f.getName());
        	String imageName = f.getName().replace(".xml", ".jpg");
        	Mat img = Imgcodecs.imread(imageSrc+"/"+ imageName);
			images.add(new CoCo_Image(1, "", imageName, img.height(), img.width(), "", image_id));
			img.release();
			
			//创建SAXReader对象
	        SAXReader reader = new SAXReader();  
	        //读取文件 转换成Document  
	        Document document = reader.read(f);
	        //获取annotation节点元素对象  
	        Element annotation = document.getRootElement();
	        //获取size节点元素对象
	        Element size = annotation.element("size");
	        int width = Integer.parseInt(size.elementText("width"));
	        int height = Integer.parseInt(size.elementText("height"));
            //获取object节点元素对象
	        ArrayList<Element>objects = (ArrayList<Element>) annotation.elements("object");
	       
	        for(Element object: objects){
	        	Element name = object.element("name");
	        	//if (name.getText().equals("person")) {
	        		
	        		List<Float> segList = new ArrayList<Float>();//初始化坐标保存队列	
					List<List<Float>> segLists = new ArrayList<>();//segmentation
		        	int category_id = 1;//category_id
		        	/*if(name.getText().equals("damaged")){
						category_id = 2;
					}*/
					/*if(name.getText().equals("yellowhat")){
							category_id = 3;
					}
					if(name.getText().equals("whitehat")){
						category_id = 4;
					}
					if(name.getText().equals("orangehat")){
						category_id = 5;
					}*/
					/*if(name.getText().equals("airplane")){
						category_id = 5;
					}
					if(name.getText().equals("oilcan")){
						category_id = 6;
					}*/
		        	Element bndbox = object.element("bndbox");
		        	float xmin = Math.round(Float.valueOf(bndbox.elementText("xmin"))*100)/100;
		        	float xmax = Math.round(Float.valueOf(bndbox.elementText("xmax"))*100)/100;
		        	float ymin = Math.round(Float.valueOf(bndbox.elementText("ymin"))*100)/100;
		        	float ymax = Math.round(Float.valueOf(bndbox.elementText("ymax"))*100)/100;    	
		        	segList.add(xmin);
					segList.add(ymin);
					segList.add(xmax);
					segList.add(ymin);
					segList.add(xmax);
					segList.add(ymax);
					segList.add(xmin);
					segList.add(ymax);
					segLists.add(segList);
					List<Float> bbox = new ArrayList<>();//bbox
					bbox.add(xmin);
					bbox.add(ymin);
					bbox.add((float)(Math.round((xmax-xmin)*100))/100);
					bbox.add((float)(Math.round((ymax-ymin)*100))/100);
					
					Float area = (xmax-xmin)*(ymax-ymin);//area
					int iscrowd = 0;//iscrowd
					annotations.add(new CoCo_Annotation(segLists, area, iscrowd, image_id, bbox, category_id, ann_id));
					ann_id ++;//id				
				//}
	        	
	        }
	        image_id++;
		}
        CoCo_Inastance inastance = new CoCo_Inastance(info, licenses, images, annotations, type, categories);
        writeFile(dst, JSONObject.toJSONString(inastance));
        //xieru
        System.out.println("完成");
	}
	public static void writeFile(String filePath, String sets) throws IOException {
		 BufferedWriter bw = new BufferedWriter(new FileWriter(  
				 filePath));// 输出新的json文件  
		 bw.write(sets);  
       // bw.newLine();       
       bw.flush();        
       bw.close();  
  }
	static{
		System.load("/usr/local/Opencv-3.3.0/share/OpenCV/java/libopencv_java330.so");
	}
}
