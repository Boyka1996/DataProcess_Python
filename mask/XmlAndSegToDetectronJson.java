package mask;
//由json文件和xml文件共同生成.json文件
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

import org.dom4j.Document;
import org.dom4j.DocumentException;
import org.dom4j.Element;
import org.dom4j.io.SAXReader;
import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.imgcodecs.Imgcodecs;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;

import JsonBean.*;

public class XmlAndSegToDetectronJson {

	@SuppressWarnings("unchecked")
	public static void main(String args[]) throws IOException, DocumentException {

		String jsonPath = "/home/chase/application/detectron/detectron/datasets/data/both/json";// json源文件路径
		String xmlPath = "/home/chase/application/detectron/detectron/datasets/data/both/xml";// xml源文件路径
		String imageSrc = "/home/chase/application/detectron/detectron/datasets/data/both/images";// 图片路径
		String savePath = "/home/chase/application/detectron/detectron/datasets/data/both/xml/hat_majia.json";// detectronJson保存文件路径
		String imageType = ".jpg";
		String[] categoriesName = {"redhat", "yellowhat", "greenhat","bluehat", "whitehat", "grayhat", "red", "yellow", "orange","blue","green","lightgreen"};



		// detectron Json字段
		CoCo_Info info = new CoCo_Info();// info
		List<CoCoLicense> licenses = new ArrayList<>();// licenses
		List<CoCo_Image> images = new ArrayList<>();// images
		List<CoCo_Annotation> annotations = new ArrayList<>();// annotations
		List<CoCoCategory> categories = new ArrayList<>();// categories
		String type = "instances";// type
		int iscrowd = 0;// iscrowd

		// 目标种类
		licenses.add(new CoCoLicense("", 1, ""));
		for (int i = 0; i < categoriesName.length; i++) {
			categories.add(new CoCoCategory(categoriesName[i], i+1, categoriesName[i]));
		}

		int image_id = 1;// 图像Id
		int ann_id = 1;// 目标Id

		for (File imageFile : new File(imageSrc).listFiles()) {
			String imageName = imageFile.getName();
			System.out.println(imageName);// 图像名
			if (!new File(xmlPath + "/" + imageName.replaceAll(imageType, ".xml")).exists() && !new File(jsonPath + "/" + imageName.replaceAll(imageType, ".json")).exists()) {
				System.out.println("图像"+imageName+"没有标签");
				continue;
			}
			Mat img = Imgcodecs.imread(imageSrc + "/" + imageName);
			images.add(new CoCo_Image(1, "", imageName, img.height(), img.width(), "", image_id));
			img.release();
			// 如果有该图像的xml标签
			if (new File(xmlPath + "/" + imageName.replaceAll(imageType, ".xml")).exists()) {
				String xmlFile = xmlPath + "/" + imageName.replaceAll(imageType, ".xml");
				System.out.println("存在xml标签" + xmlFile);

				// 创建SAXReader对象
				SAXReader reader = new SAXReader();
				// 读取文件 转换成Document
				Document document = reader.read(new File(xmlPath + "/" + imageName.replace(imageType, ".xml")));
				// 获取annotation节点元素对象
				Element annotation = document.getRootElement();
				// 获取object节点元素对象
				ArrayList<Element> objects = (ArrayList<Element>) annotation.elements("object");
				for (Element object : objects) {
					Element name = object.element("name");

					List<Float> segList = new ArrayList<Float>();// 初始化坐标保存队列
					List<List<Float>> segLists = new ArrayList<>();// segmentation
					// 获取category Id
					int category_id = getArrayId(categoriesName, name.getText());// category_id
					if (category_id == -1) {
						System.out.println("！！！！！！！！！！！！！！！ ！！！发现未定义类别" + name.getText());
						break;
					}
					Element bndbox = object.element("bndbox");
					float xmin = Math.round(Float.valueOf(bndbox.elementText("xmin")) * 100) / 100;
					float xmax = Math.round(Float.valueOf(bndbox.elementText("xmax")) * 100) / 100;
					float ymin = Math.round(Float.valueOf(bndbox.elementText("ymin")) * 100) / 100;
					float ymax = Math.round(Float.valueOf(bndbox.elementText("ymax")) * 100) / 100;
					segList.add(xmin);
					segList.add(ymin);
					segList.add(xmax);
					segList.add(ymin);
					segList.add(xmax);
					segList.add(ymax);
					segList.add(xmin);
					segList.add(ymax);
					segLists.add(segList);
					List<Float> bbox = new ArrayList<>();// bbox
					bbox.add(xmin);
					bbox.add(ymin);
					bbox.add((float) (Math.round((xmax - xmin) * 100)) / 100);
					bbox.add((float) (Math.round((ymax - ymin) * 100)) / 100);
					Float area = (xmax - xmin) * (ymax - ymin);// area
					annotations.add(new CoCo_Annotation(segLists, area, iscrowd, image_id, bbox, category_id, ann_id));
					ann_id++;// id
				}
			}

			// 如果有该图像的Json标签
			if (new File(jsonPath + "/" + imageName.replaceAll(imageType, ".json")).exists()) {
				String jsonFile = jsonPath + "/" + imageName.replaceAll(imageType, ".json");
				System.out.println("存在Json标签" + jsonFile);
				String jsonString = ReadFile(jsonFile);// 读取Json源文件
				Seg_Instance source = JSON.parseObject(jsonString, Seg_Instance.class);// Json转话为javaBean

				// xy坐标的最大最小值
				List<Seg_shape> shapes = source.getShapes();// 获取shapes字段

				// 保存坐标队列，寻找xy最大最小值
				for (int i = 0; i < shapes.size(); i++) {
					List<Float> segList = new ArrayList<Float>();// 初始化坐标保存队列
					List<List<Float>> segLists = new ArrayList<>();// segmentation
					// 获取category Id
					int category_id = getArrayId(categoriesName, shapes.get(i).getLabel());// category_id
					if (category_id == -1) {
						System.out.println("！！！！！！！！！！！！！！！！！！发现未定义类别" + shapes.get(i).getLabel());
						break;
					}
					// 获取Box Seg
					float Xmax = 0;
					float Xmin = 10000;
					float Ymax = 0;
					float Ymin = 10000;
					List<List<Float>> points = shapes.get(i).getPoints();
					for (int j = 0; j < points.size(); j++) {
						float x = (float) (Math.round(points.get(j).get(0) * 100)) / 100; // x
																							// 坐标
						float y = (float) (Math.round(points.get(j).get(1) * 100)) / 100; // y
																							// 坐标
						segList.add(x);
						segList.add(y);

						if (x > Xmax) {
							Xmax = x;
						}
						if (x < Xmin) {
							Xmin = x;
						}
						if (y > Ymax) {
							Ymax = y;
						}
						if (y < Ymin) {
							Ymin = y;
						}
					}
					segLists.add(segList);
					List<Float> bbox = new ArrayList<>();// bbox
					bbox.add(Xmin);
					bbox.add(Ymin);
					bbox.add((float) (Math.round((Xmax - Xmin) * 100)) / 100);
					bbox.add((float) (Math.round((Ymax - Ymin) * 100)) / 100);
					Float area = (Xmax - Xmin) * (Ymax - Ymin);// area
					annotations.add(new CoCo_Annotation(segLists, area, iscrowd, image_id, bbox, category_id, ann_id));
					ann_id++;// id
				}

			}
			image_id++;
		}

		CoCo_Inastance inastance = new CoCo_Inastance(info, licenses, images, annotations, type, categories);
		writeFile(savePath, JSONObject.toJSONString(inastance));
		System.out.println("wancheng");
	}

	public static String ReadFile(String path) {
		String laststr = "";
		File file = new File(path);// 打开文件
		BufferedReader reader = null;
		try {
			FileInputStream in = new FileInputStream(file);
			reader = new BufferedReader(new InputStreamReader(in, "UTF-8"));// 读取文件
			String tempString = null;
			while ((tempString = reader.readLine()) != null) {
				laststr = laststr + tempString;
			}
			reader.close();
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			if (reader != null) {
				try {
					reader.close();
				} catch (IOException el) {
				}
			}
		}
		return laststr;
	}

	public static void writeFile(String filePath, String sets) throws IOException {
		BufferedWriter bw = new BufferedWriter(new FileWriter(filePath));// 输出新的json文件
		bw.write(sets);
		// bw.newLine();
		bw.flush();
		bw.close();
	}

	// 遍历数组,获得元素下标，没有该数组，返回-1
	public static int getArrayId(String[] array, String value) {
		for (int i = 0; i < array.length; i++) {
			if (array[i].equals(value)) {
				return i + 1;
			}
		}
		return -1;// 当if条件不成立时，默认返回一个负数值-1
	}

	static {
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
	}
}
