#!/bin/sh
# ======= FILE: /usr/lib/lua/luci/view/web/index.htm ======= 
sed -i 's/>频段</><%:频段%></g' /usr/lib/lua/luci/view/web/index.htm
sed -i 's/>Wi-Fi名称</><%:Wi-Fi名称%></g' /usr/lib/lua/luci/view/web/index.htm
sed -i ':a;N;$!ba;s/>Wi-Fi密码： \n                                </><%:Wi-Fi密码：%> \n                                </g' /usr/lib/lua/luci/view/web/index.htm
sed -i 's/>连接设备数量 --</><%:连接设备数量 --%></g' /usr/lib/lua/luci/view/web/index.htm
sed -i 's/>设置</><%:设置%></g' /usr/lib/lua/luci/view/web/index.htm
sed -i ':a;N;$!ba;s/>Wi-Fi密码：\n                                </><%:Wi-Fi密码：%>\n                                </g' /usr/lib/lua/luci/view/web/index.htm
sed -i 's/>已纳入家人上网保护</><%:已纳入家人上网保护%></g' /usr/lib/lua/luci/view/web/index.htm
sed -i 's/>断开</><%:断开%></g' /usr/lib/lua/luci/view/web/index.htm
sed -i 's/'\''Mesh 组网设备'\''/'\''<%:Mesh 组网设备%>'\''/g' /usr/lib/lua/luci/view/web/index.htm
sed -i 's/'\''Mesh组网设备'\''/'\''<%:Mesh组网设备%>'\''/g' /usr/lib/lua/luci/view/web/index.htm
sed -i 's/'\''Wi-Fi名称：'\''/'\''<%:Wi-Fi名称：%>'\''/g' /usr/lib/lua/luci/view/web/index.htm
sed -i 's/'\''Wi-Fi密码: 未设置'\''/'\''<%:Wi-Fi密码: 未设置%>'\''/g' /usr/lib/lua/luci/view/web/index.htm
sed -i 's/'\''连接设备数量：'\''/'\''<%:连接设备数量：%>'\''/g' /usr/lib/lua/luci/view/web/index.htm
sed -i 's/'\''拨号成功'\''/'\''<%:拨号成功%>'\''/g' /usr/lib/lua/luci/view/web/index.htm
sed -i 's/"Mesh组网"/"<%:Mesh组网%>"/g' /usr/lib/lua/luci/view/web/index.htm
# ======= FILE: /usr/lib/lua/luci/view/web/apindex.htm ======= 
sed -i 's/>频段</><%:频段%></g' /usr/lib/lua/luci/view/web/apindex.htm
sed -i 's/>Wi-Fi名称</><%:Wi-Fi名称%></g' /usr/lib/lua/luci/view/web/apindex.htm
sed -i ':a;N;$!ba;s/>Wi-Fi密码：\n                                </><%:Wi-Fi密码：%>\n                                </g' /usr/lib/lua/luci/view/web/apindex.htm
sed -i 's/>连接设备数量 --</><%:连接设备数量 --%></g' /usr/lib/lua/luci/view/web/apindex.htm
sed -i 's/>设置</><%:设置%></g' /usr/lib/lua/luci/view/web/apindex.htm
sed -i 's/>已纳入家人上网保护</><%:已纳入家人上网保护%></g' /usr/lib/lua/luci/view/web/apindex.htm
sed -i 's/'\''Mesh组网设备'\''/'\''<%:Mesh组网设备%>'\''/g' /usr/lib/lua/luci/view/web/apindex.htm
sed -i 's/'\''Wi-Fi名称：'\''/'\''<%:Wi-Fi名称：%>'\''/g' /usr/lib/lua/luci/view/web/apindex.htm
sed -i 's/'\''Wi-Fi密码: 未设置'\''/'\''<%:Wi-Fi密码: 未设置%>'\''/g' /usr/lib/lua/luci/view/web/apindex.htm
sed -i 's/'\''连接设备数量：'\''/'\''<%:连接设备数量：%>'\''/g' /usr/lib/lua/luci/view/web/apindex.htm
sed -i 's/"Mesh组网"/"<%:Mesh组网%>"/g' /usr/lib/lua/luci/view/web/apindex.htm
# ======= FILE: /usr/lib/lua/luci/view/web/inc/g.js.htm ======= 
sed -i 's/>设置成功</><%:设置成功%></g' /usr/lib/lua/luci/view/web/inc/g.js.htm
sed -i 's/>检测到Mesh网络均为有线组网，</><%:检测到Mesh网络均为有线组网，%></g' /usr/lib/lua/luci/view/web/inc/g.js.htm
sed -i 's/>您可以开放专有回程频段以获得更好的Wi-Fi体验</><%:您可以开放专有回程频段以获得更好的Wi-Fi体验%></g' /usr/lib/lua/luci/view/web/inc/g.js.htm
sed -i 's/'\''此时5G网络已关闭'\''/'\''<%:此时5G网络已关闭%>'\''/g' /usr/lib/lua/luci/view/web/inc/g.js.htm
sed -i 's/'\''此时5G网络已打开'\''/'\''<%:此时5G网络已打开%>'\''/g' /usr/lib/lua/luci/view/web/inc/g.js.htm
sed -i 's/'\''请选择要添加的设备'\''/'\''<%:请选择要添加的设备%>'\''/g' /usr/lib/lua/luci/view/web/inc/g.js.htm
sed -i 's/'\''正在扩展Mesh节点(1-2分钟)\.\.\.'\''/'\''<%:正在扩展Mesh节点(1-2分钟)\.\.\.%>'\''/g' /usr/lib/lua/luci/view/web/inc/g.js.htm
sed -i 's/'\''正在同步Mesh节点配置\.\.\.'\''/'\''<%:正在同步Mesh节点配置\.\.\.%>'\''/g' /usr/lib/lua/luci/view/web/inc/g.js.htm
sed -i 's/'\''搜索并添加Mesh节点'\''/'\''<%:搜索并添加Mesh节点%>'\''/g' /usr/lib/lua/luci/view/web/inc/g.js.htm
sed -i 's/'\''没有搜索到可用的mesh节点'\''/'\''<%:没有搜索到可用的mesh节点%>'\''/g' /usr/lib/lua/luci/view/web/inc/g.js.htm
sed -i 's/"Redmi路由器"/"<%:Redmi路由器%>"/g' /usr/lib/lua/luci/view/web/inc/g.js.htm
sed -i 's/"小米路由器"/"<%:小米路由器%>"/g' /usr/lib/lua/luci/view/web/inc/g.js.htm
sed -i 's/"超时"/"<%:超时%>"/g' /usr/lib/lua/luci/view/web/inc/g.js.htm
# ======= FILE: /usr/lib/lua/luci/view/web/inc/header.htm ======= 
sed -i 's/>开始搜索</><%:开始搜索%></g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i ':a;N;$!ba;s/>\n             为保证Mesh网络良好的使用体验，当前至多可支持10台Mesh路由器组网，更多Mesh路由器建议组成新的Mesh网络。\n              </>\n             <%:为保证Mesh网络良好的使用体验，当前至多可支持10台Mesh路由器组网，更多Mesh路由器建议组成新的Mesh网络。%>\n              </g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/>知道了</><%:知道了%></g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i ':a;N;$!ba;s/>\n             搜索并添加Mesh节点时，请先到Wi-Fi设置页面，开启5G Wi-Fi。\n              </>\n             <%:搜索并添加Mesh节点时，请先到Wi-Fi设置页面，开启5G Wi-Fi。%>\n              </g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/>去开启</><%:去开启%></g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/>搜索Mesh子路由\.\.\.</><%:搜索Mesh子路由\.\.\.%></g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/>取消</><%:取消%></g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/>添加</><%:添加%></g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/>重试</><%:重试%></g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/>可以尝试以下方法：</><%:可以尝试以下方法：%></g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/>1、确认主路由与待添加的子路由均支持小米Mesh组网功能：</><%:1、确认主路由与待添加的子路由均支持小米Mesh组网功能：%></g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/>支持小米Mesh组网的路由产品</><%:支持小米Mesh组网的路由产品%></g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/>2、确保待添加的子路由处于未配置状态（长按Reset按钮5秒后即可恢复成未配置状态）;</><%:2、确保待添加的子路由处于未配置状态（长按Reset按钮5秒后即可恢复成未配置状态）;%></g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/>3、将待添加的子路由靠近主路由并重试（注意保持1米以外的距离以免干扰）；</><%:3、将待添加的子路由靠近主路由并重试（注意保持1米以外的距离以免干扰）；%></g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/>4、将待添加的子路由升至最新固件，并重置后重试</><%:4、将待添加的子路由升至最新固件，并重置后重试%></g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/>重新搜索</><%:重新搜索%></g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/>1、将待添加的子路由靠近主路由并重试（注意保持1米以外的距离以免干扰）；</><%:1、将待添加的子路由靠近主路由并重试（注意保持1米以外的距离以免干扰）；%></g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/>2、将主路由升至最新固件版本；</><%:2、将主路由升至最新固件版本；%></g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/>3、将待添加的子路由升至最新固件，并重置后重试（长按Reset按钮5秒后即可重置）</><%:3、将待添加的子路由升至最新固件，并重置后重试（长按Reset按钮5秒后即可重置）%></g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/>客厅</><%:客厅%></g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/>主卧</><%:主卧%></g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/>次卧</><%:次卧%></g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/>书房</><%:书房%></g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/>厨房</><%:厨房%></g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/>办公室</><%:办公室%></g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/>地下室</><%:地下室%></g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/>卫生间</><%:卫生间%></g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/>阁楼</><%:阁楼%></g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/>阳台</><%:阳台%></g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/>餐厅</><%:餐厅%></g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/>确认</><%:确认%></g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/"客厅"/"<%:客厅%>"/g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/"主卧"/"<%:主卧%>"/g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/"次卧"/"<%:次卧%>"/g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/"书房"/"<%:书房%>"/g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/"厨房"/"<%:厨房%>"/g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/"办公室"/"<%:办公室%>"/g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/"地下室"/"<%:地下室%>"/g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/"卫生间"/"<%:卫生间%>"/g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/"阁楼"/"<%:阁楼%>"/g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/"阳台"/"<%:阳台%>"/g' /usr/lib/lua/luci/view/web/inc/header.htm
sed -i 's/"餐厅"/"<%:餐厅%>"/g' /usr/lib/lua/luci/view/web/inc/header.htm
# ======= FILE: /usr/lib/lua/luci/view/web/inc/sysinfo.htm ======= 
sed -i ':a;N;$!ba;s/>\n            当前系统时间：</>\n            <%:当前系统时间：%></g' /usr/lib/lua/luci/view/web/inc/sysinfo.htm
sed -i 's/>当前系统时间：</><%:当前系统时间：%></g' /usr/lib/lua/luci/view/web/inc/sysinfo.htm
sed -i 's/>当前系统时区：</><%:当前系统时区：%></g' /usr/lib/lua/luci/view/web/inc/sysinfo.htm
sed -i 's/>\*如需修改时区，请切换到主Mesh路由进行修改，会自动同步到子Mesh路由</><%:\*如需修改时区，请切换到主Mesh路由进行修改，会自动同步到子Mesh路由%></g' /usr/lib/lua/luci/view/web/inc/sysinfo.htm
sed -i 's/>当前Wi-Fi的加密方式为超强加密（WPA3），在该模式下部分型号手机可能存在兼容性问题</><%:当前Wi-Fi的加密方式为超强加密（WPA3），在该模式下部分型号手机可能存在兼容性问题%></g' /usr/lib/lua/luci/view/web/inc/sysinfo.htm
sed -i 's/>1\. NFC功能开启</><%:1\. NFC功能开启%></g' /usr/lib/lua/luci/view/web/inc/sysinfo.htm
sed -i 's/>2\. 屏幕处于亮屏解锁的状态</><%:2\. 屏幕处于亮屏解锁的状态%></g' /usr/lib/lua/luci/view/web/inc/sysinfo.htm
# ======= FILE: /usr/lib/lua/luci/view/web/inc/wanCheck.js.htm ======= 
sed -i 's/"聚合口"/"<%:聚合口%>"/g' /usr/lib/lua/luci/view/web/inc/wanCheck.js.htm
sed -i 's/"确认是否关闭LAN口聚合功能"/"<%:确认是否关闭LAN口聚合功能%>"/g' /usr/lib/lua/luci/view/web/inc/wanCheck.js.htm
# ======= FILE: /usr/lib/lua/luci/view/web/setting/iptv.htm ======= 
