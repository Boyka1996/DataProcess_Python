package mask;
//众多由lableme程序生成的json文件合成一个json
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.imgcodecs.Imgcodecs;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;

import JsonBean.*;

public class MultiJsonToMaskJson {
	
	public static void main(String args[]) throws IOException {
		
		String srcPath ="/media/chase/YU/fzz/weilanjson/";//json源文件路径
		String imageSrc = "/media/chase/YU/fzz/weilanpic/";
		String savePath = "/media/chase/YU/fzz/weilan.json";//json保存文件路径
		
		CoCo_Info info = new CoCo_Info();//info
		List<CoCoLicense> licenses = new ArrayList<>();//licenses
		List<CoCo_Image> images = new ArrayList<>();//images
		List<CoCo_Annotation> annotations = new ArrayList<>();//annotations
		List<CoCoCategory> categories = new ArrayList<>();//categories
		String type = "instances";//type
		
		licenses.add(new CoCoLicense("", 1, ""));
		categories.add(new CoCoCategory("hengtiao", 1, "hengtiao"));
		categories.add(new CoCoCategory("lingxing", 2, "lingxing"));
		categories.add(new CoCoCategory("qizi", 3, "qizi"));
		categories.add(new CoCoCategory("wangzhuang", 4, "wangzhuang"));
		categories.add(new CoCoCategory("zhalan", 5, "zhalan"));
		//categories.add(new CoCoCategory("hat", 1, "hat"));
		//categories.add(new CoCoCategory("OFF", 2, "OFF"));
		/*
		categories.add(new Category("ear", 2, "ear"));
		categories.add(new Category("bluehat", 3, "bluehat"));
		categories.add(new Category("yellowhat", 4, "yellowhat"));
		categories.add(new Category("whitehat", 5, "whitehat"));
		categories.add(new Category("redhat", 6, "redhat"));
		*/
		int image_id=1;
		int ann_id =1;
		for (File jsonSrc:new File(srcPath).listFiles()) {
		
			String jsonString = ReadFile(jsonSrc.getAbsolutePath());//读取Json源文件									
			Seg_Instance source = JSON.parseObject(jsonString, Seg_Instance.class);//Json转话为javaBean
			
			String imageName = jsonSrc.getName().replace(".json", ".jpg");//获取imageName
			Mat img = Imgcodecs.imread(imageSrc+"/"+imageName);
			images.add(new CoCo_Image(1, "", imageName, img.height(), img.width(), "", image_id));
			img.release();
			//xy坐标的最大最小值
			
			
			List<Seg_shape>shapes = source.getShapes();//获取shapes字段
			
			//保存坐标队列，寻找xy最大最小值
			for (int i = 0; i < shapes.size(); i++) {
				List<Float> segList = new ArrayList<Float>();//初始化坐标保存队列	
				List<List<Float>> segLists = new ArrayList<>();//segmentation
				int category_id = 1;//category_id
	        	if(shapes.get(i).getLabel().equals("lingxing")){
					category_id = 2;
				}
				if(shapes.get(i).getLabel().equals("qizi")){
						category_id = 3;
				}
				if(shapes.get(i).getLabel().equals("wangzhuang")){
					category_id = 4;
				}
				if(shapes.get(i).getLabel().equals("zhalan")){
					category_id = 5;
				}
				/*int category_id = 0;//category_id
				if (shapes.get(i).getLabel().equals("ON")) {
					category_id = 1;
				}else if(shapes.get(i).getLabel().equals("OFF")) {
					category_id = 2;
				}*//*else if(shapes.get(i).getLabel().equals("yellowhat")) {
					category_id = 4;
				}else if(shapes.get(i).getLabel().equals("whitehat")) {
					category_id = 5;
				}else if(shapes.get(i).getLabel().equals("redhat")) {
					category_id = 6;
				}else if(shapes.get(i).getLabel().equals("belt")) {
					category_id = 1;
				}*/
				float Xmax = 0;
				float Xmin = 10000;
				float Ymax = 0;
				float Ymin = 10000;
				List<List<Float>> points = shapes.get(i).getPoints();
				for (int j = 0; j < points.size(); j++) {					
					float x = (float)(Math.round(points.get(j).get(0)*100))/100; //x 坐标
					float y = (float)(Math.round(points.get(j).get(1)*100))/100; //y 坐标
					segList.add(x);
					segList.add(y);
					
					if (x > Xmax) {
						Xmax  = x;
					}
					if (x < Xmin) {
						Xmin  = x;
					}
					if (y > Ymax) {
						Ymax  = y;
					}
					if (y < Ymin) {
						Ymin  = y;
					}			
				}
								
				
				segLists.add(segList);
				List<Float> bbox = new ArrayList<>();//bbox
				bbox.add(Xmin);
				bbox.add(Ymin);
				bbox.add((float)(Math.round((Xmax-Xmin)*100))/100);
				bbox.add((float)(Math.round((Ymax-Ymin)*100))/100);	
				Float area = (Xmax-Xmin)*(Ymax-Ymin);//area
				int iscrowd = 0;//iscrowd				
				System.out.println(segLists.size());
				//System.out.println(segLists.get(0).get(0));
				annotations.add(new CoCo_Annotation(segLists, area, iscrowd, image_id, bbox, category_id, ann_id));
				ann_id ++;//id
						

			}
																															
					
			image_id++;
			
		}
		CoCo_Inastance inastance = new CoCo_Inastance(info, licenses, images, annotations, type, categories);
		writeFile(savePath, JSONObject.toJSONString(inastance));		
		System.out.println("wancheng");
	}
	public static String ReadFile(String path){
		 System.out.println("kaishiyuedy");
	        String laststr="";
	        File file=new File(path);// 打开文件  
	        BufferedReader reader=null;
	        try{
	            FileInputStream in = new FileInputStream(file);
	            reader=new BufferedReader(new InputStreamReader(in,"UTF-8"));// 读取文件  
	            String tempString=null;
	            while((tempString=reader.readLine())!=null){
	                laststr=laststr+tempString;
	            }
	            reader.close();
	        }catch(IOException e){
	            e.printStackTrace();
	        }finally{
	            if(reader!=null){
	                try{
	                    reader.close();
	                }catch(IOException el){
	                }  
	            }  
	        }
	        return laststr;
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
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
	}
}
