(window.webpackJsonpfrontend=window.webpackJsonpfrontend||[]).push([[0],{152:function(e,a,t){e.exports=t(187)},158:function(e,a,t){},159:function(e,a,t){},187:function(e,a,t){"use strict";t.r(a);var n=t(0),r=t.n(n),l=t(10),o=t.n(l),c=t(249),i=t(248),m=t(13),u=(t(157),t(158),t(8)),s=t(32),d=t(50),f=(t(159),t(38)),p=t(227),E=t(228),g=t(229),h=t(46),b=t(221),v=t(102),y=t(21),O=t(226),w=t(104),_=t.n(w),k=t(59),C=t.n(k),j=t(15),S=t.n(j),x=function(e,a){return S.a.post(e,C.a.stringify(a),{headers:{"Content-Type":"application/x-www-form-urlencoded"}})},P=function(e,a){return S.a.get(e,C.a.stringify(a),{headers:{"Content-Type":"application/x-www-form-urlencoded"}})},D=r.a.createContext(),I=D.Provider,W=(D.Consumer,D),F="http://localhost:"+window.BACKEND_PORT,N=t(219),R=t(100),T=t.n(R),L=t(223),z=t(190),V=t(78),A=t(222),B=t(225),q=t(224),M=t(98),U=!1,J=function(){return U},K=function(e){return U=!!e},H=1e3,G=[],$=function(e){return G.push(e)},Q=function(e){return Object(M.a)("stepSubscribers"),G=G.filter((function(a){return a!==e}))},X=function(){return G.forEach((function(e){return e()}))},Y=["Live","Step"];var Z=function(){var e=r.a.useState(!1),a=Object(u.a)(e,2),t=a[0],n=a[1],l=r.a.useRef(null),o=r.a.useState(J()?0:1),c=Object(u.a)(o,2),i=c[0],m=c[1],s=function(e){l.current&&l.current.contains(e.target)||n(!1)};return r.a.createElement(r.a.Fragment,null,r.a.createElement(N.a,{variant:"contained",color:"primary",ref:l,"aria-label":"split button"},r.a.createElement(b.a,{onClick:function(){X()},disabled:0===i},Y[i]),r.a.createElement(b.a,{color:"primary",size:"small","aria-owns":t?"menu-list-grow":void 0,"aria-haspopup":"true",onClick:function(){n((function(e){return!e}))}},r.a.createElement(T.a,null))),r.a.createElement(A.a,{open:t,anchorEl:l.current,transition:!0,disablePortal:!0},(function(e){var a=e.TransitionProps,t=e.placement;return r.a.createElement(z.a,Object.assign({},a,{style:{transformOrigin:"bottom"===t?"center top":"center bottom"}}),r.a.createElement(V.a,{id:"menu-list-grow"},r.a.createElement(L.a,{onClickAway:s},r.a.createElement(q.a,null,Y.map((function(e,a){return r.a.createElement(B.a,{key:e,disabled:2===a,selected:a===i,onClick:function(e){return function(e,a){K(0===a),m(a),n(!1)}(0,a)}},e)}))))))})))},ee=Object(v.a)((function(e){return{appBar:Object(f.a)({marginLeft:240},e.breakpoints.up("sm"),{width:"calc(100% - ".concat(240,"px)")}),menuButton:{marginRight:e.spacing(2)},title:{flexGrow:1},logoutButton:{float:"right"}}}));var ae=function(e){var a=e.handleMenuToggle,t=void 0===a?function(){}:a,n=ee(),l=Object(y.a)(),o=Object(O.a)(l.breakpoints.up("sm")),c=r.a.useContext(W),i=r.a.useState(!1),m=Object(u.a)(i,2),f=m[0],v=m[1];return f?(x("".concat(F,"/auth/logout"),{token:c}).then((function(e){console.log(e)})).catch((function(e){console.error(e)})),localStorage.removeItem("token"),r.a.createElement(d.a,{to:"/login"})):r.a.createElement(p.a,{position:"fixed",className:n.appBar},r.a.createElement(E.a,null,!o&&r.a.createElement(r.a.Fragment,null,r.a.createElement(g.a,{color:"inherit","aria-label":"open drawer",edge:"start",onClick:t,className:n.menuButton},r.a.createElement(_.a,null)),r.a.createElement(s.b,{to:"/",style:{color:"white",textDecoration:"none"}},r.a.createElement(h.a,{variant:"h5",noWrap:!0},"Slackr"))),r.a.createElement("div",{variant:"h6",className:n.title}),r.a.createElement("div",{style:{display:"flex"}},r.a.createElement(Z,null),r.a.createElement(b.a,{color:"inherit",className:n.logoutButton,onClick:function(){v(!0)}},"Logout"))))},te=t(253),ne=t(255),re=t(230);function le(e,a){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);a&&(n=n.filter((function(a){return Object.getOwnPropertyDescriptor(e,a).enumerable}))),t.push.apply(t,n)}return t}function oe(e){for(var a=1;a<arguments.length;a++){var t=null!=arguments[a]?arguments[a]:{};a%2?le(t,!0).forEach((function(a){Object(f.a)(e,a,t[a])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):le(t).forEach((function(a){Object.defineProperty(e,a,Object.getOwnPropertyDescriptor(t,a))}))}return e}var ce=Object(v.a)((function(e){return{drawer:Object(f.a)({},e.breakpoints.up("sm"),{width:240,flexShrink:0}),drawerPaper:{width:240},toolbar:oe({},e.mixins.toolbar,{display:"flex",alignItems:"center",paddingLeft:e.spacing(2)})}}));var ie=function(e){var a=e.container,t=e.children,n=e.open,l=e.setOpen,o=ce(),c=Object(y.a)();return r.a.createElement("nav",{className:o.drawer,"aria-label":"channels"},r.a.createElement(te.a,{smUp:!0,implementation:"css"},r.a.createElement(ne.a,{container:a,variant:"temporary",anchor:"rtl"===c.direction?"right":"left",open:n,onClose:function(){return l(!1)},classes:{paper:o.drawerPaper},ModalProps:{keepMounted:!0}},r.a.createElement("div",{className:o.toolbar}),r.a.createElement(re.a,null),t)),r.a.createElement(te.a,{xsDown:!0,implementation:"css"},r.a.createElement(ne.a,{classes:{paper:o.drawerPaper},variant:"permanent",open:!0},r.a.createElement("div",{className:o.toolbar},r.a.createElement(s.b,{to:"/",style:{color:"black",textDecoration:"none"}},r.a.createElement(h.a,{variant:"h5",noWrap:!0},"Slackr"))),t)))},me=Object(v.a)((function(e){var a;return{body:(a={},Object(f.a)(a,e.breakpoints.up("sm"),{width:"calc(100% - ".concat(240,"px)")}),Object(f.a)(a,"padding",20),a),toolbar:e.mixins.toolbar}}));var ue=function(e){var a=e.children,t=me();return r.a.createElement("div",{className:t.body},r.a.createElement("div",{className:t.toolbar}),a)};var se=function(e){var a=e.menu,t=e.body,n=r.a.useState(!1),l=Object(u.a)(n,2),o=l[0],c=l[1];return r.a.createElement("div",{style:{display:"flex"}},r.a.createElement(ae,{handleMenuToggle:function(){c((function(e){return!e}))}}),r.a.createElement(ie,{open:o,setOpen:c},a),r.a.createElement(ue,null,t))},de=t(191),fe=t(192),pe=t(231),Ee=t(232),ge=t(105),he=t.n(ge);var be=function(){var e=(r.a.useContext(W),0);return r.a.createElement(de.a,null,r.a.createElement(fe.a,{button:!0,key:"profile",component:s.b,to:"/profile/".concat(e)},r.a.createElement(pe.a,null,r.a.createElement(he.a,null)),r.a.createElement(Ee.a,{primary:"Profile"})))},ve=t(241),ye=t(74),Oe=t.n(ye),we=t(75),_e=t.n(we),ke=t(106),Ce=t(233),je=t(234),Se=t(235),xe=t(236),Pe=t(237),De=t(251),Ie=t(239),We=t(256),Fe=t(240),Ne=t(110),Re=t.n(Ne),Te=t(111),Le=t.n(Te),ze=t(109),Ve=t.n(ze),Ae="An error occured. Try again later",Be="Unable to retrieve channel information";var qe=function(e){Object(ke.a)({},e);var a=r.a.useState(!1),t=Object(u.a)(a,2),n=t[0],l=t[1],o=r.a.useContext(W);function c(){l(!1)}return r.a.createElement("div",null,r.a.createElement(g.a,{size:"small",onClick:function(){l(!0)}},r.a.createElement(Ve.a,null)),r.a.createElement(Ce.a,{open:n,onClose:c,"aria-labelledby":"form-dialog-title"},r.a.createElement(je.a,{id:"form-dialog-title"},"Create Channel"),r.a.createElement("form",{onSubmit:function(e){e.preventDefault();var a=e.target[0].value,t=!e.target[1].checked;console.log(t),a&&x("".concat(F,"/channels/create"),{token:o,channel_name:a,is_public:t}).then((function(e){console.log(e)})).catch((function(e){console.error(e),m.b.error(Ae)}))}},r.a.createElement(Se.a,null,r.a.createElement(xe.a,null,"Complete the form below to create a new channel"),r.a.createElement(Pe.a,{container:!0,spacing:2,direction:"row",justify:"center",alignItems:"center"},r.a.createElement(Pe.a,{item:!0,xs:12},r.a.createElement(De.a,{autoFocus:!0,margin:"dense",id:"channel_name",label:"Channel Name",name:"channel_name",fullWidth:!0})),r.a.createElement(Pe.a,{container:!0,item:!0,justify:"center",alignItems:"center"},r.a.createElement(Re.a,null),r.a.createElement(Ie.a,{control:r.a.createElement(We.a,{value:"secret",inputProps:{"aria-label":"Secret"}}),label:"Secret",labelPlacement:"top"}),r.a.createElement(Le.a,null)))),r.a.createElement(Fe.a,null,r.a.createElement(b.a,{onClick:c,color:"primary"},"Cancel"),r.a.createElement(b.a,{onClick:c,type:"submit",color:"primary"},"Create")))))};var Me=function(e){var a=e.channel_id,t=r.a.useState([]),n=Object(u.a)(t,2),l=n[0],o=n[1],c=r.a.useState([]),i=Object(u.a)(c,2),m=i[0],d=i[1],f=r.a.useContext(W);return r.a.useEffect((function(){S.a.all([P("".concat(F,"/channels/list"),{params:{token:f}}),P("".concat(F,"/channels/listall"),{params:{token:f}})]).then(S.a.spread((function(e,a){var t=e.data.channels;console.log(t);var n=a.data.channels.filter((function(e){return void 0===t.find((function(a){return a.channel_id===e.channel_id}))}));console.log(n),o(t),d(n)})))}),[]),r.a.createElement(r.a.Fragment,null,r.a.createElement(de.a,{subheader:r.a.createElement(ve.a,{style:{display:"flex"}},r.a.createElement("span",{style:{flex:1}},"My Channels"),r.a.createElement(qe,null))},l.map((function(e,t){var n=e.channel_id,l=e.name;return r.a.createElement(fe.a,{button:!0,key:n,component:s.b,to:"/channel/".concat(n)},r.a.createElement(pe.a,null,n==a?r.a.createElement(Oe.a,null):r.a.createElement(_e.a,null)),r.a.createElement(Ee.a,{primary:l}))}))),r.a.createElement(de.a,{subheader:r.a.createElement(ve.a,null,"Other Channels")},m.map((function(e,t){var n=e.channel_id,l=e.name;return r.a.createElement(fe.a,{button:!0,key:n,component:s.b,to:"/channel/".concat(n)},r.a.createElement(pe.a,null,n==a?r.a.createElement(Oe.a,null):r.a.createElement(_e.a,null)),r.a.createElement(Ee.a,{primary:l}))}))))};var Ue=function(e){var a=e.channel_id;return r.a.createElement(r.a.Fragment,null,r.a.createElement(be,null),r.a.createElement(Me,{channel_id:a}))};var Je=function(e){return r.a.createElement(se,{menu:r.a.createElement(Ue,null),body:r.a.createElement(r.a.Fragment,null,r.a.createElement(h.a,{variant:"h4"},"WELCOME"),r.a.createElement("div",{style:{paddingTop:15}},r.a.createElement(h.a,{variant:"body1"},"This is SengChat: agile messaging for Software Engineers \u2764\ufe0f")))})},Ke=t(25),He=t(244),Ge=t(246),$e=t(121),Qe=t.n($e),Xe=t(120),Ye=t.n(Xe);var Ze=function(e){var a=e.channel_id,t=(Object(Ke.a)(e,["channel_id"]),r.a.useState(!1)),n=Object(u.a)(t,2),l=n[0],o=n[1],c=r.a.useContext(W);function i(){o(!1)}return r.a.createElement("div",null,r.a.createElement(b.a,{variant:"outlined",color:"primary",onClick:function(){o(!0)}},"Invite Member"),r.a.createElement(Ce.a,{open:l,onClose:i,"aria-labelledby":"form-dialog-title"},r.a.createElement(je.a,{id:"form-dialog-title"},"Invite User"),r.a.createElement("form",{onSubmit:function(e){e.preventDefault();var t=e.target[0].value;t&&x("".concat(F,"/channel/invite"),{token:c,user_id:t,channel_id:a}).then((function(e){console.log(e)})).catch((function(e){console.error(e),m.b.error(Ae)}))}},r.a.createElement(Se.a,null,r.a.createElement(xe.a,null,"Enter a user id below to invite a user to this channel"),r.a.createElement(De.a,{autoFocus:!0,margin:"dense",id:"user_id",label:"User ID",name:"user_id",fullWidth:!0})),r.a.createElement(Fe.a,null,r.a.createElement(b.a,{onClick:i,color:"primary"},"Cancel"),r.a.createElement(b.a,{onClick:i,type:"submit",color:"primary"},"Invite")))))},ea=t(112),aa=t.n(ea),ta=t(76),na=t.n(ta),ra=t(77),la=t(242);var oa=Object(la.a)((function(e){var a=e.message_id,t=e.is_pinned,n=void 0!==t&&t,l=e.theme,o=r.a.useState(n),c=Object(u.a)(o,2),i=c[0],m=c[1];r.a.useEffect((function(){return m(n)}),[n]);var s=r.a.useContext(W);return r.a.createElement(g.a,{onClick:function(){x("".concat(F,i?"/message/unpin":"/message/pin"),{token:s,message_id:a})},style:{margin:1},size:"small",edge:"end","aria-label":"delete"},i?r.a.createElement(na.a,{path:ra.a,size:"1em",color:l&&l.palette.action.active}):r.a.createElement(na.a,{path:ra.b,size:"1em",color:l&&l.palette.action.active}))})),ca=t(243),ia=t(113),ma=t.n(ia),ua=t(114),sa=t.n(ua);var da=function(e){var a=e.message_id,t=e.reacts,n=void 0===t?[]:t,l=r.a.useContext(W),o=0,c=!1,i=n.findIndex((function(e){return 1===e.react_id}));return-1!==i&&(o=n[i].u_ids.length,c=n[i].is_this_user_reacted),r.a.createElement(ca.a,{anchorOrigin:{horizontal:"right",vertical:"bottom"},badgeContent:o,color:"secondary"},r.a.createElement(g.a,{onClick:function(){return function(e){x("".concat(F,e?"/message/unreact":"/message/react"),{token:l,message_id:a,react_id:1})}(c)},style:{margin:1},size:"small",edge:"end","aria-label":"delete"},c?r.a.createElement(ma.a,{fontSize:"small"}):r.a.createElement(sa.a,{fontSize:"small"})))},fa=t(115),pa=t.n(fa);var Ea=function(e){var a=e.message_id,t=r.a.useContext(W);return r.a.createElement(g.a,{onClick:function(){x("".concat(F,"/message/remove"),{token:t,message_id:a})},style:{margin:1},size:"small",edge:"end","aria-label":"delete"},r.a.createElement(pa.a,{fontSize:"small"}))};var ga=function(e){var a=e.message_id,t=e.message,n=void 0===t?"":t,l=e.u_id,o=e.time_created,c=(e.is_unread,e.is_pinned),i=void 0!==c&&c,m=e.reacts,s=void 0===m?[]:m,d=r.a.useState(),f=Object(u.a)(d,2),p=f[0],E=f[1],g=r.a.useState(),h=Object(u.a)(g,2),b=h[0],v=h[1],y=r.a.useContext(W);return r.a.useEffect((function(){E(),v(),P("".concat(F,"/user/profile"),{params:{token:y,u_id:l}}).then((function(e){var a=e.data,t=(a.email,a.name_first),n=void 0===t?"":t,r=a.name_last,l=void 0===r?"":r;a.handle_str;E("".concat(n," ").concat(l)),v("".concat(n[0]).concat(l[0]))})).catch((function(e){console.error(e)}))}),[a,y,l]),r.a.createElement(fe.a,{key:a,style:{width:"100%"}},p&&b&&n&&r.a.createElement(r.a.Fragment,null,r.a.createElement(pe.a,null,r.a.createElement(He.a,null,b)),r.a.createElement("div",{style:{display:"flex",width:"100%",justifyContent:"space-between",alignItems:"center"}},r.a.createElement(Ee.a,{primary:r.a.createElement(r.a.Fragment,null,r.a.createElement("span",null,p),r.a.createElement("span",{style:{paddingLeft:10,fontSize:10}},aa()(1e3*o))),secondary:n}),r.a.createElement("div",{style:{display:"flex",height:30,marginLeft:20}},r.a.createElement(da,{message_id:a,reacts:s,u_id:l}),r.a.createElement(oa,{message_id:a,is_pinned:i}),r.a.createElement(Ea,{message_id:a})))))},ha=t(245),ba=t(119),va=t.n(ba),ya=t(118),Oa=t.n(ya),wa=t(194),_a=t(250);var ka=function(e){var a=e.open,t=e.handleClose,n=e.onTimerChange,l=(Object(Ke.a)(e,["open","handleClose","onTimerChange"]),r.a.useState(new Date)),o=Object(u.a)(l,2),c=o[0],i=o[1];return r.a.createElement("div",null,r.a.createElement(Ce.a,{open:a,onClose:t,"aria-labelledby":"form-dialog-title"},r.a.createElement(je.a,{id:"form-dialog-title"},"Send later"),r.a.createElement("form",{onSubmit:function(e){e.preventDefault(),n(c)}},r.a.createElement(Se.a,null,r.a.createElement(_a.a,{margin:"normal",id:"time-picker",label:"Time picker",value:c,onChange:function(e){return i(e.toDate())},KeyboardButtonProps:{"aria-label":"change time"}}),r.a.createElement(xe.a,null,"Enter a time to send")),r.a.createElement(Fe.a,null,r.a.createElement(b.a,{onClick:t,color:"primary"},"Cancel"),r.a.createElement(b.a,{onClick:t,type:"submit",color:"primary"},"Set Time")))))},Ca=Object(wa.a)((function(e){return{flex:{display:"flex",flexDirection:"row",alignItems:"center"},input:{margin:e.spacing(1),marginRight:0},button:{margin:e.spacing(1),marginLeft:0,alignSelf:"stretch"},rightIcon:{marginLeft:e.spacing(1)}}})),ja=-1;var Sa=function(e){var a=e.channel_id,t=void 0===a?"":a,n=Ca(),l=r.a.useState(""),o=Object(u.a)(l,2),c=o[0],i=o[1],s=r.a.useState(ja),d=Object(u.a)(s,2),f=d[0],p=d[1],E=r.a.useState(!1),h=Object(u.a)(E,2),v=h[0],y=h[1],O=r.a.useContext(W),w=f!==ja,_=function(){var e=c.trim();e&&(i(""),w?(x("".concat(F,"/message/sendlater"),{token:O,channel_id:t,message:e,time_sent:f.toISOString()}).then((function(e){var a=e.data;console.log(a)})).catch((function(e){console.error(e),m.b.error(Ae)})),p(ja)):x("".concat(F,"/message/send"),{token:O,channel_id:t,message:e}).then((function(e){var a=e.data;console.log(a)})).catch((function(e){console.error(e),m.b.error(Ae)})))};return r.a.createElement(r.a.Fragment,null,r.a.createElement("div",{className:n.flex},r.a.createElement(De.a,{className:n.input,label:"Send a message \ud83d\udcac",multiline:!0,placeholder:"...",fullWidth:!0,margin:"normal",variant:"filled",onKeyDown:function(e){"Enter"!==e.key||e.getModifierState("Shift")||(e.preventDefault(),_())},value:c,onChange:function(e){return i(e.target.value)},InputProps:{endAdornment:r.a.createElement(ha.a,{position:"end"},r.a.createElement(g.a,{"aria-label":"toggle visibility",onClick:function(){return w?p(-1):y(!0)}},r.a.createElement(Oa.a,{color:w?"secondary":void 0})))}}),r.a.createElement(b.a,{className:n.button,variant:"contained",color:"primary",onClick:_},"Send",r.a.createElement(va.a,{className:n.rightIcon}))),r.a.createElement(ka,{open:v,handleClose:function(){return y(!1)},onTimerChange:p}))};var xa=function(e){var a=e.channel_id,t=void 0===a?"":a,l=r.a.useState([]),o=Object(u.a)(l,2),c=o[0],i=o[1],s=r.a.useState(0),d=Object(u.a)(s,2),f=d[0],p=d[1],E=r.a.useContext(W),g=function(){return S.a.get("".concat(F,"/channel/messages"),{params:{token:E,channel_id:t,start:f}}).then((function(e){var a=e.data,t=a.messages,n=(a.start,a.end);p(n),i(t)})).catch((function(e){console.error(e),m.b.error(Be)}))};return r.a.useEffect((function(){return $(g),function(){return Q(g)}}),[]),function(e,a){var t=Object(n.useRef)();Object(n.useEffect)((function(){t.current=e}),[e]),Object(n.useEffect)((function(){if(null!==a){var e=setInterval((function(){t.current()}),a);return function(){return clearInterval(e)}}}),[a])}((function(){J()&&g()}),H),r.a.useEffect((function(){S.a.get("".concat(F,"/channel/messages"),{params:{token:E,channel_id:t,start:f}}).then((function(e){var a=e.data,t=a.messages,n=(a.start,a.end);p(n),i(t)})).catch((function(e){console.error(e),m.b.error(Be)}))}),[E,t,f]),r.a.createElement(r.a.Fragment,null,r.a.createElement(de.a,{subheader:r.a.createElement(ve.a,null,"Messages"),style:{width:"100%"}},c.map((function(e){return r.a.createElement(ga,e)}))),r.a.createElement(Sa,{channel_id:t}))};var Pa=function(e){var a=e.channel_id,t=(Object(Ke.a)(e,["channel_id"]),r.a.useState("")),n=Object(u.a)(t,2),l=n[0],o=n[1],c=r.a.useState([]),i=Object(u.a)(c,2),s=i[0],d=i[1],f=r.a.useState([]),p=Object(u.a)(f,2),E=p[0],v=p[1],y=r.a.useContext(W),O=0;function w(e,a){S.a.get("".concat(F,"/channel/details"),{params:{token:a,channel_id:e}}).then((function(e){var a=e.data;console.log(a);var t=a.name,n=a.owner_members,r=a.all_members;d(r),v(n),o(t)})).catch((function(e){console.error(e),m.b.error(Be)}))}function _(e,a){return void 0!==e.find((function(e){return e.u_id===a}))}r.a.useEffect((function(){w(a,y)}),[a,y]);var k=_(E,O);return r.a.createElement(r.a.Fragment,null,r.a.createElement(h.a,{variant:"h4"},l.toUpperCase()),r.a.createElement(de.a,{subheader:r.a.createElement(ve.a,null,"Members")},s.map((function(e){var t=e.u_id,n=e.name_first,l=e.name_last;return r.a.createElement(fe.a,{key:t},r.a.createElement(pe.a,null,r.a.createElement(He.a,null,n[0],l[0])),r.a.createElement(Ee.a,{primary:r.a.createElement(r.a.Fragment,null,r.a.createElement(Pe.a,{container:!0,alignItems:"center",spacing:1},r.a.createElement(Pe.a,{item:!0},r.a.createElement(Ge.a,{href:"/profile/".concat(t)},"".concat(n," ").concat(l)),"".concat(_(E,t)?" \u2b50":" ")),k&&r.a.createElement(Pe.a,{item:!0},_(E,t)?r.a.createElement(g.a,{size:"small",onClick:function(){return function(e){S.a.post("".concat(F,"/channel/removeowner"),{token:y,channel_id:a,u_id:e}).then((function(){w(a,y)})).catch((function(e){console.error(e),m.b.error(Ae)}))}(t)}},r.a.createElement(Ye.a,null)):r.a.createElement(g.a,{size:"small",onClick:function(){return function(e){S.a.post("".concat(F,"/channel/addowner"),{token:y,channel_id:a,u_id:e}).then((function(){w(a,y)})).catch((function(e){console.error(e),m.b.error(Ae)}))}(t)}},r.a.createElement(Qe.a,null)))))}))})),r.a.createElement(fe.a,{key:"invite_member"},function(e){return console.log(e),void 0!==e.find((function(e){return e.u_id===O}))}(s)?r.a.createElement(Pe.a,{container:!0,spacing:1},r.a.createElement(Pe.a,{item:!0},r.a.createElement(Ze,{channel_id:a})),r.a.createElement(Pe.a,{item:!0},r.a.createElement(b.a,{variant:"outlined",onClick:function(){return function(e,a){S.a.post("".concat(F,"/channel/leave"),{token:a,channel_id:e}).then((function(){w(e,a)})).catch((function(e){console.error(e),m.b.error(Ae)}))}(a,y)}},"Leave Channel"))):r.a.createElement(b.a,{variant:"outlined",color:"primary",onClick:function(){return function(e,a){S.a.post("".concat(F,"/channel/join"),{token:a,channel_id:e}).then((function(){w(e,a)})).catch((function(e){console.error(e),m.b.error(Ae)}))}(a,y)}},"Join Channel"))),r.a.createElement(xa,{channel_id:a}))};var Da=function(e){var a=e.match.params.channel_id;return r.a.createElement(se,{menu:r.a.createElement(Ue,{channel_id:a}),body:r.a.createElement(Pa,{channel_id:a})})},Ia=t(247),Wa=t(252),Fa=t(122),Na=t.n(Fa),Ra=Object(v.a)((function(e){return{"@global":{body:{backgroundColor:e.palette.primary.light}},card:{backgroundColor:e.palette.background.paper,marginTop:e.spacing(8),padding:e.spacing(8),display:"flex",flexDirection:"column",alignItems:"center",borderRadius:e.shape.borderRadius}}}));var Ta=function(e){var a=e.setAuth,t=Object(Ke.a)(e,["setAuth"]),n=Ra();return r.a.createElement(Ia.a,{component:"main",maxWidth:"sm"},r.a.createElement(Wa.a,{boxShadow:3,className:n.card},r.a.createElement(He.a,null,r.a.createElement(Na.a,null)),r.a.createElement(h.a,{component:"h1",variant:"h5"},"Login"),r.a.createElement("form",{noValidate:!0,onSubmit:function(e){e.preventDefault();var n=e.target[0].value,r=e.target[2].value;n&&r&&x("".concat(F,"/auth/login"),{email:n,password:r}).then((function(e){console.log(e);var n=e.data;a(n.token),t.history.push("/")})).catch((function(e){console.error(e),m.b.error(Ae)}))}},r.a.createElement(De.a,{variant:"outlined",margin:"normal",required:!0,fullWidth:!0,id:"email",label:"Email",name:"email",type:"text",autoFocus:!0}),r.a.createElement(De.a,{variant:"outlined",margin:"normal",required:!0,fullWidth:!0,name:"password",label:"Password",type:"password",id:"password",autoComplete:"current-password"}),r.a.createElement(b.a,{type:"submit",fullWidth:!0,variant:"contained",color:"primary"},"Sign In"),r.a.createElement(Pe.a,{container:!0,direction:"column",alignItems:"center"},r.a.createElement(Pe.a,{item:!0},r.a.createElement("br",null),r.a.createElement(Ge.a,{href:"/register",variant:"body1"},"Don't have an account? Register")),r.a.createElement(Pe.a,{item:!0},r.a.createElement("br",null),r.a.createElement(Ge.a,{href:"/forgot_password",variant:"body1"},"Forgot password?"))))))},La=t(55),za=t.n(La);function Va(e,a){var t=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);a&&(n=n.filter((function(a){return Object.getOwnPropertyDescriptor(e,a).enumerable}))),t.push.apply(t,n)}return t}function Aa(e){for(var a=1;a<arguments.length;a++){var t=null!=arguments[a]?arguments[a]:{};a%2?Va(t,!0).forEach((function(a){Object(f.a)(e,a,t[a])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(t)):Va(t).forEach((function(a){Object.defineProperty(e,a,Object.getOwnPropertyDescriptor(t,a))}))}return e}var Ba=Object(v.a)((function(e){return{"@global":{body:{backgroundColor:e.palette.primary.light}},card:{backgroundColor:e.palette.background.paper,marginTop:e.spacing(8),padding:e.spacing(8),display:"flex",flexDirection:"column",alignItems:"center",borderRadius:e.shape.borderRadius}}}));var qa=function(e){var a=e.setAuth,t=Object(Ke.a)(e,["setAuth"]),n=r.a.useState({name_first:"",name_last:"",email:"",password:""}),l=Object(u.a)(n,2),o=l[0],c=l[1],i=function(e){return function(a){c(Aa({},o,Object(f.a)({},e,a.target.value)))}},s=Ba();return r.a.createElement(Ia.a,{component:"main",maxWidth:"sm"},r.a.createElement(Wa.a,{boxShadow:3,className:s.card},r.a.createElement(He.a,null,r.a.createElement(za.a,{color:"secondary"})),r.a.createElement(h.a,{component:"h1",variant:"h5"},"Register"),r.a.createElement("form",{noValidate:!0,onSubmit:function(e){e.preventDefault(),o.email&&o.password&&x("".concat(F,"/auth/register"),Aa({},o)).then((function(e){console.log(e);var n=e.data;a(n.token),t.history.push("/")})).catch((function(e){console.error(e),m.b.error(Ae)}))}},r.a.createElement(De.a,{variant:"outlined",margin:"normal",required:!0,fullWidth:!0,id:"name_first",label:"First name",name:"name_first",type:"text",autoFocus:!0,value:o.name_first,onChange:i("name_first")}),r.a.createElement(De.a,{variant:"outlined",margin:"normal",required:!0,fullWidth:!0,id:"name_last",label:"Last name",name:"name_last",type:"text",value:o.name_last,onChange:i("name_last")}),r.a.createElement(De.a,{variant:"outlined",margin:"normal",required:!0,fullWidth:!0,id:"email",label:"Email",name:"email",type:"email",value:o.email,onChange:i("email")}),r.a.createElement(De.a,{variant:"outlined",margin:"normal",required:!0,fullWidth:!0,name:"password",label:"Password",type:"password",id:"password",autoComplete:"current-password",value:o.password,onChange:i("password")}),r.a.createElement(b.a,{type:"submit",fullWidth:!0,variant:"contained",color:"primary"},"Sign Up"),r.a.createElement(Pe.a,{container:!0},r.a.createElement(Pe.a,{item:!0},r.a.createElement("br",null),r.a.createElement(Ge.a,{href:"/login",variant:"body1"},"Already have an account? Login"))))))},Ma=Object(v.a)((function(e){return{"@global":{body:{backgroundColor:e.palette.primary.light}},card:{backgroundColor:e.palette.background.paper,marginTop:e.spacing(8),padding:e.spacing(8),display:"flex",flexDirection:"column",alignItems:"center",borderRadius:e.shape.borderRadius}}}));var Ua=function(e){var a=Ma();return r.a.createElement(Ia.a,{component:"main",maxWidth:"sm"},r.a.createElement(Wa.a,{boxShadow:3,className:a.card},r.a.createElement(He.a,null,r.a.createElement(za.a,{color:"secondary"})),r.a.createElement(h.a,{component:"h1",variant:"h5"},"Forgot Password"),r.a.createElement("form",{noValidate:!0,onSubmit:function(a){a.preventDefault();var t=a.target[0].value;t&&x("".concat(F,"/auth/passwordreset/request"),{email:t}).then((function(a){console.log(a),e.history.push("/reset_password")})).catch((function(e){console.error(e),m.b.error(Ae)}))}},r.a.createElement(De.a,{variant:"outlined",margin:"normal",required:!0,fullWidth:!0,id:"email",label:"Email",name:"email",type:"email",autoFocus:!0}),r.a.createElement(b.a,{type:"submit",fullWidth:!0,variant:"contained",color:"primary"},"Send Recovery Email"),r.a.createElement(Pe.a,{container:!0},r.a.createElement(Pe.a,{item:!0},r.a.createElement("br",null),r.a.createElement(Ge.a,{href:"/login",variant:"body1"},"Remember your password? Login"))))))},Ja=Object(v.a)((function(e){return{"@global":{body:{backgroundColor:e.palette.primary.light}},card:{backgroundColor:e.palette.background.paper,marginTop:e.spacing(8),padding:e.spacing(8),display:"flex",flexDirection:"column",alignItems:"center",borderRadius:e.shape.borderRadius}}}));var Ka=function(e){var a=Ja();return r.a.createElement(Ia.a,{component:"main",maxWidth:"sm"},r.a.createElement(Wa.a,{boxShadow:3,className:a.card},r.a.createElement(He.a,null,r.a.createElement(za.a,{color:"secondary"})),r.a.createElement(h.a,{component:"h1",variant:"h5"},"Reset Password"),r.a.createElement("form",{noValidate:!0,onSubmit:function(a){a.preventDefault();var t=a.target[0].value,n=a.target[2].value;t&&n&&x("".concat(F,"/auth/passwordreset/reset"),{reset_code:t,new_password:n}).then((function(a){console.log(a),e.history.push("/login")})).catch((function(e){console.error(e),m.b.error(Ae)}))}},r.a.createElement(De.a,{variant:"outlined",margin:"normal",required:!0,fullWidth:!0,id:"reset_code",label:"Reset code",name:"reset_code",type:"text",autoFocus:!0}),r.a.createElement(De.a,{variant:"outlined",margin:"normal",required:!0,fullWidth:!0,id:"new_password",label:"New Password",name:"new_password",type:"password"}),r.a.createElement(b.a,{type:"submit",fullWidth:!0,variant:"contained",color:"primary"},"Change Password"),r.a.createElement(Pe.a,{container:!0},r.a.createElement(Pe.a,{item:!0},r.a.createElement("br",null),r.a.createElement(Ge.a,{href:"/login",variant:"body1"},"Remember your password? Login"))))))},Ha=t(129),Ga=t(125),$a=t.n(Ga),Qa=t(124),Xa=t.n(Qa),Ya=t(123),Za=t.n(Ya);var et=function(e){var a=e.editable,t=e.master,n=e.masterValue,l=e.slaves,o=e.slaveValues,c=e.onSave,i=(Object(Ke.a)(e,["editable","master","masterValue","slaves","slaveValues","onSave"]),r.a.useState(!1)),m=Object(u.a)(i,2),s=m[0],d=m[1],f=r.a.useState(),p=Object(u.a)(f,2),E=p[0],g=p[1],h=r.a.useState(n),b=Object(u.a)(h,2),v=b[0],y=b[1],O=r.a.useState([]),w=Object(u.a)(O,2),_=w[0],k=w[1],C=r.a.useState(o),j=Object(u.a)(C,2),S=j[0],x=j[1];function P(){g(v),k(S),d(!s)}return r.a.createElement(Pe.a,{container:!0,spacing:1,alignItems:"flex-end"},l&&l.map((function(e,a){return r.a.createElement(Pe.a,{item:!0,key:a},e({value:S[a],InputProps:{readOnly:!s},onChange:function(e){return function(e,a){var t=S.map((function(t,n){return n===a?e.target.value:t}));x(t)}(e,a)}}))})),r.a.createElement(Pe.a,{item:!0},t({value:v,InputProps:{readOnly:!s},onChange:function(e){y(e.target.value)}})),a&&r.a.createElement(Pe.a,{item:!0},a?s?r.a.createElement(r.a.Fragment,null,r.a.createElement(Za.a,{style:{cursor:"pointer"},onClick:function(){v&&(c&&(S?c.apply(void 0,[v].concat(Object(Ha.a)(S))):c(v)),P())}}),r.a.createElement(Xa.a,{style:{cursor:"pointer"},onClick:function(){y(E),x(_),P()}})):r.a.createElement($a.a,{style:{cursor:"pointer"},onClick:P}):null))};var at=function(e){var a=e.profile,t=(Object(Ke.a)(e,["profile"]),r.a.useState({})),n=Object(u.a)(t,2),l=n[0],o=n[1],c=r.a.useContext(W),i=0;r.a.useEffect((function(){S.a.get("".concat(F,"/user/profile"),{params:{token:c,profile:a}}).then((function(e){var a=e.data;console.log(a),o(a)})).catch((function(e){console.error(e)}))}),[a,c]);var m=i.toString()===a;return r.a.createElement(r.a.Fragment,null,r.a.createElement(h.a,{variant:"h4"},"Profile"),r.a.createElement(de.a,{subheader:r.a.createElement(ve.a,null,"Profile Details")},r.a.createElement(fe.a,{key:"name"},r.a.createElement(et,{editable:m,masterValue:l.last_name,slaveValues:[l.first_name],master:function(e){return r.a.createElement(De.a,Object.assign({label:"Last Name"},e))},slaves:[function(e){return r.a.createElement(De.a,Object.assign({label:"First Name"},e))}],onSave:function(e,a){S.a.put("".concat(F,"/user/profile/setname"),{token:c,name_first:a,name_last:e}).then((function(){console.log("all good")})).catch((function(e){console.error(e)}))}})),r.a.createElement(fe.a,{key:"email"},r.a.createElement(et,{editable:m,masterValue:l.email,master:function(e){return r.a.createElement(De.a,Object.assign({label:"Email"},e))},onSave:function(e){S.a.put("".concat(F,"/user/profile/setemail"),{token:c,email:e}).then((function(){console.log("all good")})).catch((function(e){console.error(e)}))}})),r.a.createElement(fe.a,{key:"handle"},r.a.createElement(et,{editable:m,masterValue:"phlips",master:function(e){return r.a.createElement(De.a,Object.assign({label:"Handle"},e))},onSave:function(e){S.a.put("".concat(F,"/user/profile/sethandle"),{token:c,handle:e}).then((function(){console.log("all good")})).catch((function(e){console.error(e)}))}}))))};var tt=function(e){var a=e.match.params.profile;return r.a.createElement(se,{menu:r.a.createElement(Ue,null),body:r.a.createElement(at,{profile:a})})};var nt=function(e){var a=r.a.useContext(W);return console.log(a),a?r.a.createElement(d.b,e):r.a.createElement(d.a,{to:"/login"})};var rt=function(){var e=r.a.useState(localStorage.getItem("token")),a=Object(u.a)(e,2),t=a[0],n=a[1];function l(e){localStorage.setItem("token",e),n(e)}return r.a.createElement(I,{value:t},r.a.createElement(s.a,null,r.a.createElement(d.d,null,r.a.createElement(d.b,{exact:!0,path:"/login",render:function(e){return r.a.createElement(Ta,Object.assign({},e,{setAuth:l}))}}),r.a.createElement(d.b,{exact:!0,path:"/register",render:function(e){return r.a.createElement(qa,Object.assign({},e,{setAuth:l}))}}),r.a.createElement(d.b,{exact:!0,path:"/forgot_password",component:Ua}),r.a.createElement(d.b,{exact:!0,path:"/reset_password",component:Ka}),r.a.createElement(nt,{exact:!0,path:"/",component:Je}),r.a.createElement(nt,{path:"/profile/:profile",component:tt}),r.a.createElement(nt,{path:"/channel/:channel_id",component:Da}))))};Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));var lt=t(68),ot=t(128),ct=Object(ot.a)({palette:{primary:{main:"#556cd6"},secondary:{main:"#19857b"},error:{main:lt.a.A400},background:{default:"#fff"}}}),it=t(22),mt=t(126);o.a.render(r.a.createElement(i.a,{theme:ct},r.a.createElement(it.a,{utils:mt.a},r.a.createElement(c.a,null),r.a.createElement(rt,null),r.a.createElement(m.a,{position:"top-center",autoClose:5e3,hideProgressBar:!1,newestOnTop:!0,closeOnClick:!0,rtl:!1,pauseOnVisibilityChange:!0,draggable:!0,pauseOnHover:!0}))),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()}))}},[[152,1,2]]]);
//# sourceMappingURL=main.fd883b1b.chunk.js.map