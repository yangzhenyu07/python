
create table t_job_info
(
    SEQUENCE_NO int auto_increment comment '序列号'
        primary key,
    POSITION varchar(255) not null comment '岗位',
    REGION varchar(255) not null comment '区域',
    CITY varchar(255) not null comment '城市',
    SALARY varchar(50) not null comment '薪资',
    EXPERIENCE varchar(50) null comment '年限信息',
    COMPANY_NAME varchar(255) null comment '公司名称',
    COMPANY_INFO TEXT null comment '公司信息',
    LEVEL varchar(50) null comment '3-5年为1,5到-10年为0',
    CREATE_TIME datetime default CURRENT_TIMESTAMP not null comment '创建时间'

)
comment 'boss 存储表';