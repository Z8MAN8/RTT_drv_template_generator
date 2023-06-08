# 引用所需的库（字符串操作和正则表达式）
import os
import re
from datetime import datetime

print("目前支持版本为RT-Thread 5.0.0 其他版本需要自行检查ops")
# 获取用户输入
print("支持：i2c soft_i2c spi soft_spi gpio usart pwm adc dac tim wdt tim rtc")
drv_name_input = input("请输入要对接的驱动（例如i2c、soft_i2c等）: ")
chip_name_input = input("请输入板卡类型（例如stm32、lpc、st7796）: ")
user_name_input = input("请输入昵称: ")

# 构造文件名
c_file = "drv_" + drv_name_input + ".c"
h_file = "drv_" + drv_name_input + ".h"

# 定义文件内容模板
c_template = '''/*
 * Copyright (c) 2006-2023, RT-Thread Development Team
 *
 * SPDX-License-Identifier: Apache-2.0
 *
 * Change Logs:
 * Date           Author       Notes
 * {date}        {user_name}    the first version
 */

#include "{h_file}"
/* 更多头文件自定义添加 */

#ifdef BSP_USING_{drv_name_upper}
#define DBG_TAG              "drv.{drv}"
#define DBG_LVL               DBG_INFO
#include <rtdbg.h>

static struct {chip}_{drv}_config {drv}_config[] =
{{
#ifdef BSP_USING_{drv_name_upper}0
    {drv_name_upper}0_CONFIG,
#endif
/* 如有多个同类外设可在此自定义添加 */
}};

static struct {chip}_{drv} {chip}_{drv}_obj[sizeof({drv}_config) / sizeof({drv}_config[0])];

{ops}

int rt_hw_{drv}_init(void)
{{
    int result = RT_EOK;

    /* 自定义填入 */

    for (rt_size_t i = 0; i < sizeof({chip}_{drv}_obj) / sizeof(struct {chip}_{drv}); i++)
    {{
        /* 自定义填入 */

        /* register {drv} device */
        if (/* 自定义填入rtt相关注册函数 */) == RT_EOK)
        {{
            LOG_D("%s init success", /* 自定义填入 */);
        }}
        else
        {{
            LOG_E("%s register failed", /* 自定义填入 */);
            result = -RT_ERROR;
        }}
    }}

    return result;
}}
INIT_/* 自定义填入 */_EXPORT(rt_hw_{drv}_init);

'''

h_template = '''/*
 * Copyright (c) 2006-2023, RT-Thread Development Team
 *
 * SPDX-License-Identifier: Apache-2.0
 *
 * Change Logs:
 * Date           Author       Notes
 * {date}        {user_name}    the first version
 */

#ifndef {filename_upper}
#define {filename_upper}

#ifdef BSP_USING_{drv_name_upper}
#include <rtdevice.h>
/* 更多头文件自定义添加 */

/* {chip} {drv} config */
struct {chip}_{drv}_config
{{
    /* 自定义填入 */
}};

/* {chip} {drv} driver class */
struct {chip}_{drv}
{{
    /* 自定义填入 */
}};

#ifdef BSP_USING_{drv_name_upper}0
#define {drv_name_upper}0_CONFIG
    {{
        /* 自定义填入 */
    }}
#endif /* BSP_USING_{drv_name_upper}0 */

int rt_hw_{drv}_init(void);

#endif /* BSP_USING_{drv_name_upper} */
#endif  /* {filename_upper} */

'''

# 定义文件编码格式
encoding = 'utf-8'

# 获取当前日期并格式化为YYYY-MM-DD形式
current_date = datetime.now().strftime("%Y-%m-%d")

# 根据条件进行替换
if drv_name_input == "sof_i2c":
    ops_template = '''
/**
 * This function sets the sda pin.
 *
 * @param {chip} config class.
 * @param The sda pin state.
 */
static void {chip}_set_sda(void *data, rt_int32_t state)
{
    /* 自定义填入 */
}

/**
 * This function sets the scl pin.
 *
 * @param {chip} config class.
 * @param The scl pin state.
 */
static void {chip}_set_scl(void *data, rt_int32_t state)
{
    /* 自定义填入 */
}

/**
 * This function gets the sda pin state.
 *
 * @param The sda pin state.
 */
static rt_int32_t {chip}_get_sda(void *data)
{
    /* 自定义填入 */
}

/**
 * This function gets the scl pin state.
 *
 * @param The scl pin state.
 */
static rt_int32_t {chip}_get_scl(void *data)
{
    /* 自定义填入 */
}

/**
 * The time delay function.
 *
 * @param microseconds.
 */
static void {chip}_udelay(rt_uint32_t us)
{
    /* 自定义填入 */
}

static const struct rt_i2c_bit_ops {chip}_bit_ops_default =
{
    .data     = RT_NULL,
    .set_sda  = {chip}_set_sda,
    .set_scl  = {chip}_set_scl,
    .get_sda  = {chip}_get_sda,
    .get_scl  = {chip}_get_scl,
    .udelay   = {chip}_udelay,
    .delay_us = 1,
    .timeout  = 100
};
'''

elif drv_name_input == "i2c":
    ops_template = '''
rt_ssize_t {chip}_i2c_xfer(struct rt_i2c_bus_device *bus,
                             struct rt_i2c_msg msgs[],
                             rt_uint32_t num)
{
    /* 自定义填入 */
}

static const struct rt_i2c_bus_device_ops i2c_ops =
{
    .master_xfer      = {chip}_i2c_xfer,
    .slave_xfer       = RT_NULL,
    .i2c_bus_control  = RT_NULL
};
'''

elif drv_name_input == "spi":
    ops_template = '''
static rt_ssize_t spixfer(struct rt_spi_device *device, struct rt_spi_message *message)
{
    /* 自定义填入 */
}

static rt_err_t spi_configure(struct rt_spi_device *device,
                              struct rt_spi_configuration *configuration)
{
    /* 自定义填入 */
}

static const struct rt_spi_ops {chip}_spi_ops =
{
    .configure = spi_configure,
    .xfer = spixfer,
};
'''

elif drv_name_input == "soft_spi":
    ops_template = '''
void {chip}_tog_sclk(void *data)
{
    /* 自定义填入 */
}

void {chip}_set_sclk(void *data, rt_int32_t state)
{
    /* 自定义填入 */
}

void {chip}_set_mosi(void *data, rt_int32_t state)
{
    /* 自定义填入 */
}

void {chip}_set_miso(void *data, rt_int32_t state)
{
    /* 自定义填入 */
}

rt_int32_t {chip}_get_sclk(void *data)
{
    /* 自定义填入 */
}

rt_int32_t {chip}_set_mosi(void *data)
{
    /* 自定义填入 */
}

rt_int32_t {chip}_get_miso(void *data)
{
    /* 自定义填入 */
}

void {chip}_dir_mosi(void *data, rt_int32_t state)
{
    /* 自定义填入 */
}

void {chip}_dir_miso(void *data, rt_int32_t state)
{
    /* 自定义填入 */
}

void {chip}_udelay(rt_uint32_t us)
{
    /* 自定义填入 */
}

static struct rt_spi_bit_ops {chip}_soft_spi_ops =
{
    .data = RT_NULL,
    .tog_sclk = {chip}_tog_sclk,
    .set_sclk = {chip}_set_sclk,
    .set_mosi = {chip}_set_mosi,
    .set_miso = {chip}_set_miso,
    .get_sclk = {chip}_get_sclk,
    .get_mosi = {chip}_get_mosi,
    .get_miso = {chip}_get_miso,
    .dir_mosi = {chip}_dir_mosi,
    .dir_miso = {chip}_dir_miso,
    .udelay = {chip}_udelay,
    .delay_us = 1,
};
'''

elif drv_name_input == "gpio":
    ops_template = '''
void {chip}_pin_mode(struct rt_device *device, rt_base_t pin, rt_uint8_t mode)
{
    /* 自定义填入 */
}

void {chip}_pin_write(struct rt_device *device, rt_base_t pin, rt_uint8_t value)
{
    /* 自定义填入 */
}

rt_int8_t {chip}_pin_read(struct rt_device *device, rt_base_t pin)
{
    /* 自定义填入 */
}

rt_err_t {chip}_pin_attach_irq(struct rt_device *device, rt_base_t pin,
            rt_uint8_t mode, void (*hdr)(void *args), void *args)
{
    /* 自定义填入 */
}

rt_err_t {chip}_pin_dettach_irq(struct rt_device *device, rt_base_t pin)
{
    /* 自定义填入 */
}

rt_err_t {chip}_pin_irq_enable(struct rt_device *device, rt_base_t pin, rt_uint8_t enabled)
{
    /* 自定义填入 */
}

rt_base_t {chip}_pin_get(const char *name)
{
    /* 自定义填入 */
}

static const struct rt_pin_ops _{chip}_pin_ops =
{
    .pin_mode = {chip}_pin_mode,
    .pin_write = {chip}_pin_write,
    .pin_read = {chip}_pin_read,
    .pin_attach_irq = {chip}_pin_attach_irq,
    .pin_detach_irq = {chip}_pin_dettach_irq,
    .pin_irq_enable = {chip}_pin_irq_enable,
    .pin_get = {chip}_pin_get,
};
'''

elif drv_name_input == "pwm":
    ops_template = '''
rt_err_t drv_pwm_control(struct rt_device_pwm *device, int cmd, void *arg)
{
    /* 自定义填入 */
}

static struct rt_pwm_ops drv_ops =
{
    .control = drv_pwm_control
};
'''

elif drv_name_input == "wdt":
    ops_template = '''
static rt_err_t wdt_init(rt_watchdog_t *wdt)
{
    /* 自定义填入 */
}

static rt_err_t wdt_control(rt_watchdog_t *wdt, int cmd, void *arg)
{
    /* 自定义填入 */
}

static const struct rt_watchdog_ops ops =
{
    .init    = wdt_init,
    .control = wdt_control,
};
'''

elif drv_name_input == "tim":
    ops_template = '''
void timer_init(struct rt_hwtimer_device *timer, rt_uint32_t state)
{
    /* 自定义填入 */
}

rt_err_t timer_start(struct rt_hwtimer_device *timer, rt_uint32_t cnt, rt_hwtimer_mode_t mode)
{
    /* 自定义填入 */
}

void timer_stop(struct rt_hwtimer_device *timer)
{
    /* 自定义填入 */
}

rt_uint32_t timer_counter_get(struct rt_hwtimer_device *timer)
{
    /* 自定义填入 */
}

rt_err_t timer_ctrl(struct rt_hwtimer_device *timer, rt_uint32_t cmd, void *args)
{
    /* 自定义填入 */
}

static const struct rt_hwtimer_ops {chip}_tim_ops =
{
    .init = timer_init,
    .start = timer_start,
    .stop = timer_stop,
    .count_get = timer_counter_get,
    .control = timer_ctrl,
};
'''

elif drv_name_input == "rtc":
    ops_template = '''
rt_err_t {chip}_rtc_init(void)
{
    /* 自定义填入 */
}

rt_err_t {chip}_rtc_get_secs(time_t *sec)
{
    /* 自定义填入 */
}

rt_err_t {chip}_rtc_set_secs(time_t *sec)
{
    /* 自定义填入 */
}

rt_err_t {chip}_rtc_get_alarm(struct rt_rtc_wkalarm *alarm)
{
    /* 自定义填入 */
}

rt_err_t {chip}_rtc_set_alarm(struct rt_rtc_wkalarm *alarm)
{
    /* 自定义填入 */
}

rt_err_t {chip}_rtc_get_timeval(struct timeval *tv)
{
    /* 自定义填入 */
}

static const struct rt_rtc_ops {chip}_rtc_ops =
{
    .init        = {chip}_rtc_init,
    .get_secs    = {chip}_rtc_get_secs,
    .set_secs    = {chip}_rtc_set_secs,
    .get_alarm   = {chip}_rtc_get_alarm,
    .set_alarm   = {chip}_rtc_set_alarm,
    .get_timeval = {chip}_rtc_get_timeval,
    .set_timeval = RT_NULL,
};
'''

elif drv_name_input == "usart":
    ops_template = '''
rt_err_t {chip}_configure(struct rt_serial_device *serial, struct serial_configure *cfg)
{
    /* 自定义填入 */
}

rt_err_t {chip}_control(struct rt_serial_device *serial, int cmd, void *arg)
{
    /* 自定义填入 */
}

int {chip}_putc(struct rt_serial_device *serial, char c)
{
    /* 自定义填入 */
}

int {chip}_getc(struct rt_serial_device *serial)
{
    /* 自定义填入 */
}

rt_ssize_t {chip}_dma_transmit(struct rt_serial_device *serial, rt_uint8_t *buf, rt_size_t size, int direction)
{
    /* 自定义填入 */
}

static const struct rt_uart_ops {chip}_uart_ops =
{
    .configure = {chip}_configure,
    .control = {chip}_control,
    .putc = {chip}_putc,
    .getc = {chip}_getc,
    .dma_transmit = {chip}_dma_transmit
};
'''

elif drv_name_input == "dac":
    ops_template = '''
rt_err_t {chip}_dac_disabled(struct rt_dac_device *device, rt_uint32_t channel)
{
    /* 自定义填入 */
}

rt_err_t {chip}_dac_enabled(struct rt_dac_device *device, rt_uint32_t channel)
{
    /* 自定义填入 */
}

rt_err_t {chip}_set_dac_value(struct rt_dac_device *device, rt_uint32_t channel, rt_uint32_t *value)
{
    /* 自定义填入 */
}

rt_uint8_t {chip}_dac_get_resolution(struct rt_dac_device *device)
{
    /* 自定义填入 */
}

static const struct rt_dac_ops stm_dac_ops =
{
    .disabled = {chip}_dac_disabled,
    .enabled  = {chip}_dac_enabled,
    .convert  = {chip}_set_dac_value,
    .get_resolution = {chip}_dac_get_resolution,
};
'''

elif drv_name_input == "adc":
    ops_template = '''
static rt_err_t {chip}_{drv}_enabled(struct rt_adc_device *device, rt_int8_t channel, rt_bool_t enabled)
{
    /* 自定义填入 */
}

static rt_err_t {chip}_{drv}_get_value(struct rt_adc_device *device, rt_int8_t channel, rt_uint32_t *value)
{
    /* 自定义填入 */
}

rt_uint8_t {chip}_{drv}_get_resolution(struct rt_adc_device *device)
{
    /* 自定义填入 */
}

rt_int16_t {chip}_{drv}_get_vref(struct rt_adc_device *device)
{
    /* 自定义填入 */
}

static const struct rt_{drv}_ops {chip}_{drv}_ops =
{
    .enabled = {chip}_{drv}_enabled,
    .convert = {chip}_{drv}_get_value,
    .get_resolution = {chip}_{drv}_get_resolution,
    .get_vref = {chip}_{drv}_get_vref,
};
'''
else:
    print("不支持的驱动类型")

# 生成.c文件
with open(c_file, 'w', encoding=encoding) as file:
    file.write(c_template.format(date=current_date, \
    h_file=h_file, \
    user_name=user_name_input, \
    chip=chip_name_input, \
    drv=drv_name_input, \
    drv_name_upper=re.sub(r'\.', '_', drv_name_input.upper()), \
    filename_upper=re.sub(r'\.', '_', h_file.upper()), \
    ops=ops_template.replace("{drv}", drv_name_input).replace("{chip}", chip_name_input)
    ))

# 生成.h文件
with open(h_file, 'w', encoding=encoding) as file:
    file.write(h_template.format(date=current_date, \
    user_name=user_name_input, \
    chip=chip_name_input, \
    drv=drv_name_input, \
    drv_name_upper=re.sub(r'\.', '_', drv_name_input.upper()), \
    filename_upper=re.sub(r'\.', '_', h_file.upper())))

print("文件生成完成！")
