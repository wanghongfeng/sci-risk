package com.sci.risk.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.License;
import io.swagger.v3.oas.models.servers.Server;
import io.swagger.v3.oas.models.tags.Tag;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.List;

@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("供应链控制塔 API")
                        .description("供应链控制塔关税风险模拟系统 API 文档，支持关税风险模拟、风险场景分析等多种算法服务")
                        .version("1.0.0")
                        .contact(new Contact()
                                .name("SCI Team")
                                .email("support@sci.com"))
                        .license(new License()
                                .name("Apache 2.0")
                                .url("https://www.apache.org/licenses/LICENSE-2.0")))
                .servers(List.of(
                        new Server().url("https://weak-zondra-laosha007-8931c4eb.koyeb.app").description("Koyeb 服务器")
                ))
                .tags(List.of(
                        new Tag().name("模拟服务").description("关税风险模拟相关接口"),
                        new Tag().name("算法管理").description("算法注册与发现接口"),
                        new Tag().name("任务管理").description("任务状态查询接口"),
                        new Tag().name("菜单管理").description("系统菜单维护接口")
                ));
    }
}