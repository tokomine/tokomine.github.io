---
title: Java Spring 笔记
date: 2022-09-28 16:51:05
categories: 
- 笔记
tags:
- Java
- Spring
---
# 各种概念
## 什么是IoC
- IoC（Inverse of Control，控制反转），即某一接口具体实现类的选择控制权从调用类中移除，转交给第三方决定，即由Spring容器借由Bean配置来进行控制。  
- 也可以用 DI（De-pendency Injection，依赖注入）的概念用来代替IoC，即让调用类对某一接口实现类的依赖关系由第三方（容器或协作类）注入，以移除调用类对某一接口实现类的依赖。“

## 什么是JavaBean
一种说法是：
1. 所有属性为private
2. 提供默认构造方法
3. 提供getter和setter
4. 实现serializable接口

另一种说法：
JavaBean实际上是指一种特殊的Java类，它通常用来实现一些比较常用的简单功能，并可以很容易的被重用或者是插入其他应用程序中去。所有遵循“一定编程原则”的Java类都可以被称作JavaBean。JavaBean是一个遵循特定写法的Java类，是一种Java语言编写的可重用组件，它的方法命名，构造及行为必须符合特定的约定：
1. 这个类必须具有一个公共的(public)无参构造函数；
2. 所有属性私有化（private）；
3. 私有化的属性必须通过public类型的方法（getter和setter）暴露给其他程序，并且方法的命名也必须遵循一定的命名规范。 
4. 这个类应是可序列化的。（比如可以实现Serializable 接口，用于实现bean的持久性）

## 什么是POJO
一种说法是：一个简单的Java类，这个类没有实现/继承任何特殊的java接口或者类，不遵循任何主要java模型，约定或者框架的java对象。在理想情况下，POJO不应该有注解。
另一种说法是：POJO是一个简单的、普通Java对象，它包含业务逻辑处理或持久化逻辑等，但不是JavaBean、EntityBean等，不具有任何特殊角色，不继承或不实现任何其它Java框架的类或接口。

## 什么是DAO类
一种说法是：DAO (DataAccessobjects 数据存取对象)是指位于业务逻辑和持久化数据之间实现对持久化数据的访问。通俗来讲，就是将数据库操作都封装起来。

## 什么是AOP
AOP是Aspect Oriented Programing的简称，“面向切面编程”。

## 什么是CGLIB
CGLIB是一个功能强大，高性能的代码生成包。它为没有实现接口的类提供代理，为JDK的动态代理提供了很好的补充。通常可以使用Java的动态代理创建代理，但当要代理的类没有实现接口或者为了更好的性能，CGLIB是一个好的选择。

# 资源访问
## Resource 接口
Spring设计了一个Resource接口，它为应用提供了更强的底层资源访问能力。Spring框架使用Resource装载各种资源，包括配置文件资源、国际化属性文件资源等。具体实现类：
- WritableResource：可写资源接口，是Spring 3.1版本新加的接口，有两个实现类，即FileSystemResource和PathResource，其中PathResource是Spring 4.0提供的实现类。
  - FileSystemResource：文件系统资源，资源以文件系统路径的方式表示，如D:/conf/bean.xml等。
  - PathResource：Spring 4.0提供的读取资源文件的新类。Path封装了java.net.URL、java.nio.file.Path（Java 7.0提供）、文件系统资源，它使用户能够访问任何可以通过URL、Path、系统文件路径表示的资源，如文件系统的资源、HTTP资源、FTP资源等。
- ByteArrayResource：二进制数组表示的资源，二进制数组资源可以在内存中通过程序构造。
- ClassPathResource：类路径下的资源，资源以相对于类路径的方式表示。
- InputStreamResource：以输入流返回表示的资源。
- ServletContextResource：为访问Web容器上下文中的资源而设计的类，负责以相对于Web应用根目录的路径加载资源。它支持以流和URL的方式访问，在WAR解包的情况下，也可以通过File方式访问。该类还可以直接从JAR包中访问资源。
- UrlResource：URL封装了java.net.URL，它使用户能够访问任何可以通过URL表示的资源，如文件系统的资源、HTTP资源、FTP资源等。
资源加载时默认采用系统编码读取资源内容。如果资源文件采用特殊的编码格式，那么可以通过EncodedResource对资源进行编码，以保证资源内容操作的正确性。


## ResourceLoader 接口

加载所有类包com.smart（及子孙包）下以.xml为后缀的资源
```JAVA
ResourcePatternResolver resolver = newPathMatchingResourcePatternResolver();
Resource resources[] = resolver.getResources("classpath*:com/smart/**/*.xml");
```
JAR包中要使用getInputStream，而不是getFile
```JAVA
(new DefaultResourceLoader()).getResource("classpath:conf/sys.properties").getInputStream()
```


# BeanFactory和ApplicationContext
## 介绍
BeanFactory一般称为IoC容器，提供了高级IoC的配置机制。在初始化BeanFactory时，必须为其提供一种日志框架。
而称ApplicationContext为应用上下文，也称为Spring容器。在BeanFactory基础之上，提供了更多面向应用的功能，它提供了国际化支持和框架事件体系，更易于创建实际应用。

## BeanFactory的类体系结构
最主要的方法就是getBean(String beanName)，该方法从容器中返回特定名称的Bean。主要派生有：
- ListableBeanFactory：该接口定义了访问容器中Bean基本信息的若干方法，如查看Bean的个数、获取某一类型Bean的配置名、查看容器中是否包括某一Bean等。
- HierarchicalBeanFactory：父子级联IoC容器的接口，子容器可以通过接口方法访问父容器。
- ConfigurableBeanFactory：这是一个重要的接口，增强了IoC容器的可定制性。它定义了设置类装载器、属性编辑器、容器初始化后置处理器等方法。
- AutowireCapableBeanFactory：定义了将容器中的Bean按某种规则（如按名字匹配、按类型匹配等）进行自动装配的方法。
- SingletonBeanRegistry：定义了允许在运行期向容器注册单实例Bean的方法。
- BeanDefinitionRegistry：Spring配置文件中每一个bean节点元素在Spring容器里都通过一个BeanDefinition对象表示，它描述了Bean的配置信息。而BeanDefinition Reg-istry接口提供了向容器手工注册BeanDefinition对象的方法。
  
## ApplicationContext类体系结构
ApplicationContext在初始化应用上下文时就实例化所有单实例的Bean。  
主要实现类是：
- ClassPathXmlApplicationContext，默认从类路径加载配置文件。
- FileSystemXmlApplicationContext，默认从文件系统中装载配置文件。

```JAVA
ApplicationContext ctx = new ClassPathXmlApplicationContext("xxx/beans.xml");
Car car = ctx.getBean("car",Car.class);
```

## 基于类注解的配置

```JAVA
//①表示是一个配置信息提供类
@Configuration
public class Beans {
    //②定义一个Bean     
    @Bean(name = "car")     
    public Car buildCar() {
        Car car = new Car();
        car.setBrand("红旗CA72");
        car.setMaxSpeed(200);
        return car;
    }
}
```

## Bean的生命周期

![BeanFactory中Bean的生命周期](/images/post/BeanFactory中Bean的生命周期.png)

- Bean自身的方法：如调用Bean构造函数实例化Bean、调用Setter设置Bean的属性值及通过bean的init-method和destroy-method所指定的方法。
- Bean级生命周期接口方法：如BeanNameAware、Bean-FactoryAware、InitializingBean和DisposableBean，这些接口方法由Bean类直接实现。
- 容器级生命周期接口方法：在图4-11中带“★”的步骤是由InstantiationAwareBean PostProcessor和BeanPost-Processor这两个接口实现的，一般称它们的实现类为“后处理器”。后处理器接口一般不由Bean本身实现，它们独立于Bean，实现类以容器附加装置的形式注册到Spring容器中，并通过接口反射为Spring容器扫描识别。当Spring容器创建任何Bean的时候，这些后处理器都会发生作用，所以这些后处理器的影响是全局性的。当然，用户可以通过合理地编写后处理器，让其仅对感兴趣的Bean进行加工处理。
- 工厂后处理器接口方法：包括AspectJWeavingEnabler、CustomAutowireConfigurer、ConfigurationClassPostPro-cessor等方法。工厂后处理器也是容器级的，在应用上下文装配配置文件后立即调用。


如果在bean中指定Bean的作用范围为scope="prototype"，则将Bean返回给调用者，调用者负责Bean后续生命的管理，Spring不再管理这个Bean的生命周期。如果将作用范围设置为scope="singleton"，则将Bean放入SpringIoC容器的缓存池中，并将Bean引用返回给调用者，Spring继续对这些Bean进行后续的生命管理。    

ApplicationContext会利用Java反射机制自动识别出配置文件中定义的BeanPostProcessor、InstantiationAwareBeanPost Processor和BeanFactoryPostProcessor，并自动将它们注册到应用上下文中。
```JAVA
public class MyBeanFactoryPostProcessor implements BeanFactoryPostProcessor{
    //①对car <bean>的brand属性配置信息进行“偷梁换柱”的加工操作
    public void postProcessBeanFactory(ConfigurableListableBeanFactory bf)        throws BeansException {
        BeanDefinition bd = bf.getBeanDefinition("car");
        bd.getPropertyValues().addPropertyValue("brand", "奇瑞QQ");
        System.out.println("调用BeanFactoryPostProcessor.postProcessBean Factory()！");
    }
}
```

```XML
<!--①这个brand属性的值将被工厂后处理器更改掉-->
<bean id="car" class="com.smart.Car" init-method="myInit" destroy-method="myDestory"
      p:brand="红旗CA72"
      p:maxSpeed="200"/>
<!--②工厂后处理器-->
<bean id="myBeanPostProcessor"
      class="com.smart.context.MyBeanPostProcessor"/>
<!--③注册Bean后处理器-->
<bean id="myBeanFactoryPostProcessor"
      class="com.smart.context.MyBeanFactoryPostProcessor"/>
```

# 在IoC容器中装配Bean
## 基于XML的配置文件
### 基本配置
```XML
<?xml version="1.0" encoding="UTF-8" ?>
<beans   xmlns="http://www.springframework.org/schema/beans"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"          
          xsi:schemaLocation="http://www.springframework.org/schema/beans         
          http://www.springframework.org/schema/beans/spring-beans-4.0.xsd">
    <bean id="car" class="com.smart.simple.Car"/>
    <bean id="boss" class="com.smart.simple.Boss"/>
</beans>
```
### 属性注入
```XML
<bean id="car" class="com.smart.ditype.Car">
    <property name="maxSpeed"><value>200</value></property>    
    <property name="brand"><value>红旗CA72</value></property>    
    <property name="price"><value>20000.00</value></property>
</bean>
```

### 构造函数注入
1. 按类型匹配
```XML
<bean id="car1" class="com.smart.ditype.Car">
    <constructor-arg type="java.lang.String">
        <value>红旗CA72</value>
    </constructor-arg>
    <constructor-arg type="double">
        <value>20000</value>
    </constructor-arg>
</bean>
```
2. 按索引匹配
```XML
<bean id="car2" class="com.smart.ditype.Car">
    <!--①注意索引从0开始-->
    <constructor-arg index="0" value="红旗CA72"/>
    <constructor-arg index="1" value="中国一汽"/>
    <constructor-arg index="2" value="20000"/>
</bean>
```

### 工厂注入
1. 非静态工厂
```XML
<!--①工厂类Bean -->
<bean id="carFactory" class="com.smart.ditype.CarFactory"/>
<!-- factory-bean指定①处的工厂类Bean； factory-method指定工厂类Bean创建该Bean的工厂方法-->
<bean id="car5"  factory-bean="carFactory"
                 factory-method="createHongQiCar"/>
```

2. 静态工厂
```XML
<bean id="car6"  class="工厂类"
                 factory-method="createCar"/>
```

### 整合多个配置文件
```XML
<import resource="classpath:com/smart/impt/beans1.xml"/>
<bean id="boss1" class="com.smart.fb.Boss" p:name="John" p:car-ref="car1"/>
<bean id="boss2" class="com.smart.fb.Boss" p:name="John" p:car-ref="car2"/>
```


## 基于注解的配置
### Component
@Component注解在类声明处对类进行标注，它可以被Spring容器识别，Spring容器自动将POJO转换为容器管理的Bean。  
它和以下XML配置是等效的：
```XML
<bean id="id" class="xxx.class"/>
```

### Autowired
- 使用@Autowired进行自动注入。默认按类型（byType）匹配的方式在容器中查找匹配的Bean，当有且仅有一个匹配的Bean时成功。  
- 如果希望Spring即使找不到匹配的Bean完成注入也不要抛出异常，那么可以使用@Autowired(required=false)进行标注。  
- 可以通过@Qualifier注解限定Bean的名称。
```JAVA
@Service
public class LogonService {
    @Autowired   
    private LogDao logDao;  
    
    //①注入名为userDao、类型为UserDao的Bean   
    @Autowired   
    @Qualifier("userDao")   
    private UserDao userDao;    
}
```

@Autowired可以对类成员变量及方法的入参进行标注。
```JAVA
@Service
public class LogonService {    
    private LogDao logDao;    
    private UserDao userDao;    
    
    //①自动将LogDao传给方法入参    
    @Autowired    
    public void setLogDao(LogDao logDao) {        
        this.logDao = logDao;    
    }    
    
    //②自动将名为userDao的Bean传给方法入参    
    @Autowired    
    @Qualifier("userDao")    
    public void setUserDao(UserDao userDao) {        
        this.userDao = userDao;    
    }
}
```
对类中集合类的变量或方法入参进行@Autowired标注，那么Spring会将容器中类型匹配的所有Bean都自动注入进来。
```JAVA
@Component
public class MyComponent {    
    //①Spring会将容器中所有类型为Plugin的Bean注入这个变量中     
    @Autowired(required=false)     
    private List<Plugin> plugins;    
    //②将Plugin类型的Bean注入Map中      
    @Autowired      
    private Map<String,Plugin> pluginMaps;      
    public List<Plugin> getPlugins() {                
        return plugins;      
    }
}
```


### Scope
指定Bean的作用范围。
```JAVA
//①指定Bean的作用范围为prototype
@Scope("prototype")
@Component
public class Car {
    …
}

```

### PostConstruct和PreDestroy
指定Bean的初始化及容器销毁前执行的方法。
```JAVA
@PostConstruct        
private void init1(){
    System.out.println("execute in init1");        
}        
@PreDestroy        
private void destory1(){
    System.out.println("execute in destory1");    
}
```

### Configuration
普通的POJO只要标注@Configuration注解，就可以为Spring容器提供Bean定义的信息，每个标注了@Bean的类方法都相当于提供了一个Bean的定义信息。
```JAVA
//①将一个POJO标注为定义Bean的配置类
@Configuration
public class AppConf {    
    //②以下两个方法定义了两个Bean，并提供了Bean的实例化逻辑    
    @Bean
    public UserDao userDao(){
        return new UserDao();    
    }    
    
    @Bean    
    public LogDao logDao(){        
        return new LogDao();    
    }   
    //③定义了logonService的Bean   
    @Bean    
    public LogonService logonService(){        
        LogonService logonService = new LogonService();      
        //④ 将②和③处定义的Bean注入logonService Bean中        
        logonService.setLogDao(logDao());        
        logonService.setUserDao(userDao());        
        return logonService;    
    }
}
```

Spring提供了一个AnnotationConfigApplicationContext类，它能够直接通过标注@Configuration的Java类启动Spring容器。
```JAVA
ApplicationContext ctx = new AnnotationConfigApplicationContext(AppConf.class);
```

AnnotationConfigApplicationContext还支持通过编码的方式加载多个@Configuration配置类，然后通过刷新容器应用这些配置类。
```JAVA
AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext();           
//①注册多个@Configuration配置类           
ctx.register(DaoConfig.class);           
ctx.register(ServiceConfig.class);           
//②刷新容器以应用这些注册的配置类            
ctx.refresh();
```

