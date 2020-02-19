package mask;

import java.io.File;
import java.io.IOException;
import java.net.UnknownHostException;

import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.imgcodecs.Imgcodecs;

import xml.XML;

public class MaskResultToXml {
	
	private static MaskRCNN mask;
	public static String imagePath = "/devdata/dataset/luneng/xianjia/luomu/images";
	public static String savePath = "/devdata/dataset/luneng/xianjia/luomu/Annotations";
	
	public static void main(String args[]) throws UnknownHostException, IOException {
		
		mask = new MaskRCNN("localhost", 8080);
		XML xml = new XML();
		
		for (File img : new File(imagePath).listFiles()) {
			
			String result = mask.detect(img.getAbsolutePath());
			if (!result.equals("")) {
				
			    Mat mat = Imgcodecs.imread(img.getAbsolutePath());
			    int height = mat.height();
			    int width = mat.width();
			    xml.saveXML(width, height, savePath+"/"+img.getName().replace("jpg", "xml"), result);
			    mat.release();
				
			}
			
		}						
	}
	
	static {
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
	}

}
