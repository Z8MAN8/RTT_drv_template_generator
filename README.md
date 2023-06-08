# RTT_drv_template_generator RT-Thread设备驱动模板生成工具

### 如果喜欢请Star，这是对本开源项目最大的鼓励，谢谢
---------

本工具用于生成对接 RT-Thread 设备框架的 drv_.c/.h 文件：

- 目前兼容 RT-Thread 5.0.0 其他版本需要检查操作方法是否一致

- 支持：i2c soft_i2c spi soft_spi gpio usart pwm adc dac tim wdt tim rtc


- 用户针对自己的板卡，实现对应的操作方法即可
- 会在当前目录生成 drv_.c/.h 文件，自行复制到对应的位置，scons 和 Kconfig 文件需要自行修改

## 使用方法

### 方法一

直接运行脚本,根据提示信息,输入 **驱动类型** ，**板卡类型** ，**昵称** 即可。

``` shell
▸ python drv_template.py
请输入要对接的驱动（例如i2c、soft_i2c等）: rtc
请输入板卡类型（例如stm32、lpc、st7796）: pico
请输入昵称: chu
```

### 注意

软件i2c和spi输入格式：soft_i2c、soft_spi

推荐搭配 [formating](https://github.com/mysterywolf/formatting) 工具一起使用

## 使用协议

本软件为MIT协议，可以自由免费使用，无论是个人目的还是商业目的，但是发现本脚本有任何问题，请提PR协助修复。
