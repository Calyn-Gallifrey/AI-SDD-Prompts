# 目标
本规则用于根据背景和要求开发 OM API 防腐层代码。

# 背景
## 背景1：API接口设计文档
+ 用户输入：{包路径}
+ 用户输入：{业务功能描述}
+ 用户输入：{外部API接口信息}

## 背景2：防腐层开发规范
* 防腐层通过独立的Helper工具类和Parser解析类来实现入参组装和返回值转换
* Helper类负责构建外部API的请求参数和解析返回结果
* Parser类负责将外部API的复杂响应对象转换为业务VO对象
* 使用RemoteResultUtil工具类处理远程调用结果
* 使用Optional代替返回null，避免空指针异常
* Service层只负责业务流程编排，不包含具体的参数构建和解析逻辑

## 示例1:Service接口定义
```
package com.ocft.iic.uaw.server.modules.transaction.support.agreement.service;

import com.ocft.iic.uaw.server.modules.transaction.common.pojo.bo.QueryAgreementBO;
import com.ocft.iic.uaw.server.modules.transaction.common.agreement.pojo.vo.AgreementVO;

import java.util.List;

/**
 * 协议查询服务
 * @author EX-YUANLEI246
 */
public interface QueryAgreementService {

    /**
     * 调用接口，获取协议信息
     * @param bo 客户信息参数
     * @return AgreementVO
     */
    List<AgreementVO> queryAgreement(QueryAgreementBO bo);
}
```

## 示例2:Service实现类
```
package com.ocft.iic.uaw.server.modules.transaction.support.agreement.service.impl;

import com.google.common.collect.Lists;
import com.ocft.iic.ohs.Result;
import com.ocft.iic.third.api.api.OmCustomerServiceAcl;
import com.ocft.iic.third.api.dto.req.GetParamBO;
import com.ocft.iic.third.api.dto.rsp.Portfolio;
import com.ocft.iic.uaw.server.modules.transaction.common.pojo.bo.QueryAgreementBO;
import com.ocft.iic.uaw.server.modules.transaction.common.agreement.pojo.vo.AgreementVO;
import com.ocft.iic.uaw.server.modules.transaction.common.service.queryagreement.QueryAgreementService;
import com.ocft.iic.uaw.server.modules.transaction.common.helper.queryagreement.QueryAgreementHelper;
import com.ocft.iic.uaw.server.modules.transaction.support.utils.RemoteResultUtil;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

/**
 * 协议查询服务实现
 * @author EX-YUANLEI246
 */
@Slf4j
@Service
public class QueryAgreementServiceImpl implements QueryAgreementService {

    @Autowired
    private OmCustomerServiceAcl omCustomerServiceAcl;

    @Override
    public List<AgreementVO> queryAgreement(QueryAgreementBO bo) {
        // 构建OM的API集成防腐层服务入参
        GetParamBO param = QueryAgreementHelper.buildParam(bo);
        // 构建OM的API集成防腐层获取结果，断言结果如果为空默认抛出远程调用异常
        Result<Portfolio> result = omCustomerServiceAcl.portfolioList(param);
        RemoteResultUtil.throwIfNotSuccess(result);
        // 解析结果转换成业务VO对象
        Optional<List<AgreementVO>> agreementOpt = QueryAgreementHelper.convertResult(result);
        return agreementOpt.orElse(Lists.newArrayList());
    }
}
```

## 示例3:Helper工具类
```
package com.ocft.iic.uaw.server.modules.transaction.support.agreement.helper;

import com.ocft.iic.ohs.Result;
import com.ocft.iic.third.api.dto.req.GetParamBO;
import com.ocft.iic.third.api.dto.rsp.Portfolio;
import com.ocft.iic.uaw.server.modules.transaction.common.pojo.bo.QueryAgreementBO;
import com.ocft.iic.uaw.server.modules.transaction.common.agreement.pojo.vo.AgreementVO;
import com.ocft.iic.uaw.server.modules.transaction.support.utils.RemoteResultUtil;
import lombok.extern.slf4j.Slf4j;
import java.util.List;
import java.util.Optional;

/**
 * 协议查询辅助工具类
 * @author EX-YUANLEI246
 */
@Slf4j
public class QueryAgreementHelper {

    /**
     * 构建协议查询入参ACL参数，输入客户号进行查询
     *
     * @param bo 查询协议BO
     * @return GetParamBO
     */
    public static GetParamBO buildParam(QueryAgreementBO bo) {
        GetParamBO param = new GetParamBO();
        param.setParams(new String[]{bo.getCustomerNumber()});
        return param;
    }

    /**
     * 将 Portfolio 响应转换为 AgreementVO
     *
     * @param alcQueryResult Portfolio 响应结果
     * @return AgreementVO 对象
     */
    public static Optional<List<AgreementVO>> convertResult(Result<Portfolio> alcQueryResult) {
        Optional<Portfolio> portfolioOpt = RemoteResultUtil.parseData(alcQueryResult);
        if (!portfolioOpt.isPresent()) {
            return Optional.empty();
        }
        AgreementParser parser = new AgreementParser(portfolioOpt.get());
        return parser.parse();
    }

}
```

## 示例4:Parser解析类
```
package com.ocft.iic.uaw.server.modules.transaction.support.agreement.helper;

import com.baomidou.mybatisplus.core.toolkit.CollectionUtils;
import com.ocft.iic.third.api.dto.rsp.Portfolio;
import com.ocft.iic.uaw.server.modules.transaction.common.agreement.pojo.vo.AgreementVO;
import com.ocft.iic.uaw.server.modules.transaction.common.agreement.pojo.vo.CoverageVO;
import com.ocft.iic.uaw.server.modules.transaction.common.agreement.pojo.vo.LifeVO;
import com.ocft.iic.uaw.server.modules.transaction.common.agreement.pojo.vo.PolicyVO;
import lombok.extern.slf4j.Slf4j;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Optional;

/**
 * 协议解析器
 * @author CHUQIUSHI731
 */
@Slf4j
public class AgreementParser {

    private List<Portfolio.PortfolioResponseInner.GetPortfolioResponse.Agreement> agreements;

    public AgreementParser(Portfolio portfolio) {
        agreements = portfolio.getPortfolioResponse()
                .getGetPortfolioResponse()
                .getAgreement();
    }

    public Optional<List<AgreementVO>> parse() {
        if (CollectionUtils.isEmpty(agreements)) {
            log.warn("convertResult agreements isEmpty");
            return Optional.empty();
        }
        List<AgreementVO> vos = new ArrayList<>();
        for (Portfolio.PortfolioResponseInner.GetPortfolioResponse.Agreement agreement : agreements) {
            vos.add(buildAgreementVO(agreement));
        }
        return Optional.ofNullable(vos);
    }

    private static AgreementVO buildAgreementVO(Portfolio.PortfolioResponseInner.GetPortfolioResponse.Agreement
                                                        agreement) {
        AgreementVO result = new AgreementVO();
        // 设置基本字段
        result.setAgreementName(agreement.getAgreementName());
        result.setCarrierAdminSystem(agreement.getCarrierAdminSystem());
        result.setProductSystemId(agreement.getProductSystemId());
        // 设置 agreementStatus
        result.setAgreementStatus(getAgreementStatus(agreement));
        // 设置错误信息
        result.setErrorInfo(getErrorInfo(agreement));
        // 设置 Policy 信息
        result.setPolicy(getPolicy(agreement));
        return result;
    }

    private static List<Portfolio.PortfolioResponseInner.GetPortfolioResponse.Agreement.ErrorInfo> getErrorInfo(
            Portfolio.PortfolioResponseInner.GetPortfolioResponse.Agreement agreement) {
        if (agreement.getErrorInfo() == null) {
            return Collections.emptyList();
        }
        return agreement.getErrorInfo();
    }

    private static String getAgreementStatus(Portfolio.PortfolioResponseInner.GetPortfolioResponse.Agreement agreement) {
        if (agreement.getAgreementStatus() == null) {
            return null;
        }
        return agreement.getAgreementStatus().getValue();
    }

    /**
     * 将 Agreement 的 Policy 转换为 PolicyVO
     */
    private static PolicyVO getPolicy(Portfolio.PortfolioResponseInner.GetPortfolioResponse.Agreement agreement) {
        Portfolio.PortfolioResponseInner.GetPortfolioResponse.Agreement.Policy policy = agreement.getPolicy();
        if (policy == null) {
            return null;
        }
        PolicyVO policyVO = new PolicyVO();
        // 设置policyVO属性信息
        policyVO.setPolNumber(policy.getPolNumber());
        policyVO.setProductCode(policy.getProductCode());
        policyVO.setProductType(getProductType(policy.getProductType()));
        // 处理 Life 信息
        policyVO.setLife(getLife(policy.getLife()));
        return policyVO;
    }

    /**
     * 将 Policy.Life 转换为 LifeVO
     */
    private static LifeVO getLife(Portfolio.PortfolioResponseInner.GetPortfolioResponse.Agreement.Policy.Life life) {
        if (life == null) {
            return null;
        }
        LifeVO lifeVO = new LifeVO();
        lifeVO.setCashValueAmt(life.getCashValueAmt());
        // 处理 Coverage 列表
        lifeVO.setCoverage(getCoverages(life.getCoverage()));
        return lifeVO;
    }

    /**
     * 将 Life.Coverage 列表转换为 CoverageVO 列表
     */
    private static List<CoverageVO> getCoverages(
            List<Portfolio.PortfolioResponseInner.GetPortfolioResponse.Agreement.Policy.Life.Coverage> coverages) {
        if (CollectionUtils.isEmpty(coverages)) {
            return Collections.emptyList();
        }
        List<CoverageVO> coverageVOs = new ArrayList<>();
        for (Portfolio.PortfolioResponseInner.GetPortfolioResponse.Agreement.Policy.Life.Coverage coverage : coverages) {
            CoverageVO coverageVO = new CoverageVO();
            coverageVO.setCurrentAmt(coverage.getCurrentAmt());
            coverageVOs.add(coverageVO);
        }
        return coverageVOs;
    }

    /**
     * 将 ProductType 枚举转换为 String 值
     */
    private static String getProductType(Portfolio.PortfolioResponseInner.GetPortfolioResponse.Agreement.Policy.ProductType type) {
        return type != null ? type.getValue() : null;
    }
}
```

## 示例5:RemoteResultUtil工具类使用
```
package com.ocft.iic.uaw.server.util;

import cn.hutool.json.JSONUtil;
import com.ocft.iic.ecommon.api.enums.IICResEnum;
import com.ocft.iic.ecommon.api.exception.IICRuntimeException;
import com.ocft.iic.ohs.Result;
import lombok.extern.slf4j.Slf4j;

import java.util.Optional;

/**
 * 远程结果工具类
 *
 * @author CHUQIUSHI731
 */
@Slf4j
public class RemoteResultUtil {

    /**
     * 如果Result不成功则抛出异常
     *
     * @param result 结果对象
     * @param <T> 泛型类型
     */
    public static <T> void throwIfNotSuccess(Result<T> result) {
        if (!Result.isSuccess(result)) {
            log.warn("portfolioList failed: {}", result.getResponseMessage());
            throw new IICRuntimeException(IICResEnum.REMOTE_SERVICE_FAIL);
        }
    }

    /**
     * 解析Result返回Optional的data
     *
     * @param result 结果对象
     * @param <T> 泛型类型
     * @return Optional<T>
     */
    public static <T> Optional<T> parseData(Result<T> result) {
        if (result == null || result.getData() == null) {
            log.warn("om acl result parseData is null");
            return Optional.empty();
        }
        log.info("om acl result is : {}", JSONUtil.toJsonStr(result));
        return Optional.of(result.getData());
    }
}
```

# 要求
1. 根据背景1获取用户输入的包路径、业务功能描述、外部API接口信息
2. 根据背景2和示例创建Service接口、Service实现类、Helper工具类、Parser解析类
3. Service层只负责业务流程编排，调用Helper进行参数构建和结果解析
4. Helper类负责构建外部API请求参数和调用Parser进行结果转换
5. Parser类负责将外部API的复杂响应对象转换为业务VO对象
6. 使用RemoteResultUtil.throwIfNotSuccess()检查远程调用结果，失败时抛出异常
7. 使用RemoteResultUtil.parseData()解析远程调用结果，返回Optional对象
8. 使用Optional代替返回null，避免空指针异常
9. 对于可能为null的对象，使用Optional.empty()或Optional.ofNullable()包装
10. 对于集合对象，为空时返回Collections.emptyList()或Lists.newArrayList()
11. 放到对应位置，如果没有则新建，windows系统
 