
create table t_yzy_test
(
    SEQUENCE_NO int auto_increment comment '序列号'
        primary key,
    PK_STD_POINT_AI_RELATION varchar(36) not null comment 'id',
    FK_STD_AUDIT_POINT varchar(36) not null comment '审核标准id',
    FK_AI_STD varchar(36) not null comment 'aiId',
    CHANNEL_TAG varchar(45) not null comment '渠道',
    FK_USER_CREATE varchar(36) null comment '创建人id',
    USER_NAME_CREATE varchar(64) null comment '创建人姓名',
    CREATE_TIME datetime default CURRENT_TIMESTAMP not null comment '创建时间',
    constraint u_t_yzy_test_00
        unique (PK_STD_POINT_AI_RELATION),
    constraint u_t_yzy_test_01
        unique (FK_STD_AUDIT_POINT, FK_AI_STD, CHANNEL_TAG)
)
comment '测试表';


create index i_t_yzy_test_00
    on t_yzy_test (FK_STD_AUDIT_POINT);


create index i_t_yzy_test_01
    on t_yzy_test(FK_AI_STD);