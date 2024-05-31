import{l as y,b0 as se,b7 as w,j as m,b1 as I,p as f,a2 as h,k as V,q as E,v as z,n as g,b as s,A as le,F as T,ae as de,af as re,z as L,T as oe,a8 as ce,b8 as D,ar as N}from"./index-DsUmHdtM.js";import{l as P,c as F,H as ue,q as $,w as R,o as H,f as O,W as ve,a as q,n as A,g as C,x as j,m as ye,b as me,J as fe,D as ge,E as be,s as he,R as ke,d as Se,e as Ce,K as Ve,G as xe,F as Ae,v as Ie,L as Pe}from"./VGrid-CxerTJ5w.js";function pe(e){let l=arguments.length>1&&arguments[1]!==void 0?arguments[1]:"div",n=arguments.length>2?arguments[2]:void 0;return y()({name:n??se(w(e.replace(/__/g,"-"))),props:{tag:{type:String,default:l},...m()},setup(t,r){let{slots:d}=r;return()=>{var a;return I(t.tag,{class:[e,t.class],style:t.style},(a=d.default)==null?void 0:a.call(d))}}})}const _e=f({start:Boolean,end:Boolean,icon:h,image:String,text:String,...m(),...P(),...F(),...ue(),...V(),...E(),...$({variant:"flat"})},"VAvatar"),B=y()({name:"VAvatar",props:_e(),setup(e,l){let{slots:n}=l;const{themeClasses:t}=z(e),{colorClasses:r,colorStyles:d,variantClasses:a}=R(e),{densityClasses:i}=H(e),{roundedClasses:u}=O(e),{sizeClasses:v,sizeStyles:o}=ve(e);return g(()=>s(e.tag,{class:["v-avatar",{"v-avatar--start":e.start,"v-avatar--end":e.end},t.value,r.value,i.value,u.value,v.value,a.value,e.class],style:[d.value,o.value,e.style]},{default:()=>[n.default?s(C,{key:"content-defaults",defaults:{VImg:{cover:!0,image:e.image},VIcon:{icon:e.icon}}},{default:()=>[n.default()]}):e.image?s(q,{key:"image",src:e.image,alt:"",cover:!0},null):e.icon?s(A,{key:"icon",icon:e.icon},null):e.text,j(!1,"v-avatar")]})),{}}}),Te=y()({name:"VCardActions",props:m(),setup(e,l){let{slots:n}=l;return le({VBtn:{slim:!0,variant:"text"}}),g(()=>{var t;return s("div",{class:["v-card-actions",e.class],style:e.style},[(t=n.default)==null?void 0:t.call(n)])}),{}}}),Le=f({opacity:[Number,String],...m(),...V()},"VCardSubtitle"),Be=y()({name:"VCardSubtitle",props:Le(),setup(e,l){let{slots:n}=l;return g(()=>s(e.tag,{class:["v-card-subtitle",e.class],style:[{"--v-card-subtitle-opacity":e.opacity},e.style]},n)),{}}}),we=pe("v-card-title"),Ee=f({appendAvatar:String,appendIcon:h,prependAvatar:String,prependIcon:h,subtitle:[String,Number],title:[String,Number],...m(),...P()},"VCardItem"),ze=y()({name:"VCardItem",props:Ee(),setup(e,l){let{slots:n}=l;return g(()=>{var v;const t=!!(e.prependAvatar||e.prependIcon),r=!!(t||n.prepend),d=!!(e.appendAvatar||e.appendIcon),a=!!(d||n.append),i=!!(e.title!=null||n.title),u=!!(e.subtitle!=null||n.subtitle);return s("div",{class:["v-card-item",e.class],style:e.style},[r&&s("div",{key:"prepend",class:"v-card-item__prepend"},[n.prepend?s(C,{key:"prepend-defaults",disabled:!t,defaults:{VAvatar:{density:e.density,image:e.prependAvatar},VIcon:{density:e.density,icon:e.prependIcon}}},n.prepend):s(T,null,[e.prependAvatar&&s(B,{key:"prepend-avatar",density:e.density,image:e.prependAvatar},null),e.prependIcon&&s(A,{key:"prepend-icon",density:e.density,icon:e.prependIcon},null)])]),s("div",{class:"v-card-item__content"},[i&&s(we,{key:"title"},{default:()=>{var o;return[((o=n.title)==null?void 0:o.call(n))??e.title]}}),u&&s(Be,{key:"subtitle"},{default:()=>{var o;return[((o=n.subtitle)==null?void 0:o.call(n))??e.subtitle]}}),(v=n.default)==null?void 0:v.call(n)]),a&&s("div",{key:"append",class:"v-card-item__append"},[n.append?s(C,{key:"append-defaults",disabled:!d,defaults:{VAvatar:{density:e.density,image:e.appendAvatar},VIcon:{density:e.density,icon:e.appendIcon}}},n.append):s(T,null,[e.appendIcon&&s(A,{key:"append-icon",density:e.density,icon:e.appendIcon},null),e.appendAvatar&&s(B,{key:"append-avatar",density:e.density,image:e.appendAvatar},null)])])])}),{}}}),De=f({opacity:[Number,String],...m(),...V()},"VCardText"),Ne=y()({name:"VCardText",props:De(),setup(e,l){let{slots:n}=l;return g(()=>s(e.tag,{class:["v-card-text",e.class],style:[{"--v-card-text-opacity":e.opacity},e.style]},n)),{}}}),Fe=f({appendAvatar:String,appendIcon:h,disabled:Boolean,flat:Boolean,hover:Boolean,image:String,link:{type:Boolean,default:void 0},prependAvatar:String,prependIcon:h,ripple:{type:[Boolean,Object],default:!0},subtitle:[String,Number],text:[String,Number],title:[String,Number],...ye(),...m(),...P(),...de(),...me(),...fe(),...ge(),...be(),...F(),...he(),...V(),...E(),...$({variant:"elevated"})},"VCard"),Oe=y()({name:"VCard",directives:{Ripple:ke},props:Fe(),setup(e,l){let{attrs:n,slots:t}=l;const{themeClasses:r}=z(e),{borderClasses:d}=Se(e),{colorClasses:a,colorStyles:i,variantClasses:u}=R(e),{densityClasses:v}=H(e),{dimensionStyles:o}=re(e),{elevationClasses:b}=Ce(e),{loaderClasses:x}=Ve(e),{locationStyles:M}=xe(e),{positionClasses:W}=Ae(e),{roundedClasses:K}=O(e),k=Ie(e,n),X=L(()=>e.link!==!1&&k.isLink.value),S=L(()=>!e.disabled&&e.link!==!1&&(e.link||k.isClickable.value));return g(()=>{const Y=X.value?"a":e.tag,Q=!!(t.title||e.title!=null),U=!!(t.subtitle||e.subtitle!=null),Z=Q||U,ee=!!(t.append||e.appendAvatar||e.appendIcon),te=!!(t.prepend||e.prependAvatar||e.prependIcon),ae=!!(t.image||e.image),ne=Z||te||ee,ie=!!(t.text||e.text!=null);return oe(s(Y,{class:["v-card",{"v-card--disabled":e.disabled,"v-card--flat":e.flat,"v-card--hover":e.hover&&!(e.disabled||e.flat),"v-card--link":S.value},r.value,d.value,a.value,v.value,b.value,x.value,W.value,K.value,u.value,e.class],style:[i.value,o.value,M.value,e.style],href:k.href.value,onClick:S.value&&k.navigate,tabindex:e.disabled?-1:void 0},{default:()=>{var p;return[ae&&s("div",{key:"image",class:"v-card__image"},[t.image?s(C,{key:"image-defaults",disabled:!e.image,defaults:{VImg:{cover:!0,src:e.image}}},t.image):s(q,{key:"image-img",cover:!0,src:e.image},null)]),s(Pe,{name:"v-card",active:!!e.loading,color:typeof e.loading=="boolean"?void 0:e.loading},{default:t.loader}),ne&&s(ze,{key:"item",prependAvatar:e.prependAvatar,prependIcon:e.prependIcon,title:e.title,subtitle:e.subtitle,appendAvatar:e.appendAvatar,appendIcon:e.appendIcon},{default:t.item,prepend:t.prepend,title:t.title,subtitle:t.subtitle,append:t.append}),ie&&s(Ne,{key:"text"},{default:()=>{var _;return[((_=t.text)==null?void 0:_.call(t))??e.text]}}),(p=t.default)==null?void 0:p.call(t),t.actions&&s(Te,null,{default:t.actions}),j(S.value,"v-card")]}}),[[ce("ripple"),S.value&&e.ripple]])}),{}}}),$e=f({disabled:Boolean,group:Boolean,hideOnLeave:Boolean,leaveAbsolute:Boolean,mode:String,origin:String},"transition");function c(e,l,n){return y()({name:e,props:$e({mode:n,origin:l}),setup(t,r){let{slots:d}=r;const a={onBeforeEnter(i){t.origin&&(i.style.transformOrigin=t.origin)},onLeave(i){if(t.leaveAbsolute){const{offsetTop:u,offsetLeft:v,offsetWidth:o,offsetHeight:b}=i;i._transitionInitialStyles={position:i.style.position,top:i.style.top,left:i.style.left,width:i.style.width,height:i.style.height},i.style.position="absolute",i.style.top=`${u}px`,i.style.left=`${v}px`,i.style.width=`${o}px`,i.style.height=`${b}px`}t.hideOnLeave&&i.style.setProperty("display","none","important")},onAfterLeave(i){if(t.leaveAbsolute&&(i!=null&&i._transitionInitialStyles)){const{position:u,top:v,left:o,width:b,height:x}=i._transitionInitialStyles;delete i._transitionInitialStyles,i.style.position=u||"",i.style.top=v||"",i.style.left=o||"",i.style.width=b||"",i.style.height=x||""}}};return()=>{const i=t.group?D:N;return I(i,{name:t.disabled?"":e,css:!t.disabled,...t.group?void 0:{mode:t.mode},...t.disabled?{}:a},d.default)}}})}function G(e,l){let n=arguments.length>2&&arguments[2]!==void 0?arguments[2]:"in-out";return y()({name:e,props:{mode:{type:String,default:n},disabled:Boolean,group:Boolean},setup(t,r){let{slots:d}=r;const a=t.group?D:N;return()=>I(a,{name:t.disabled?"":e,css:!t.disabled,...t.disabled?{}:l},d.default)}})}function J(){let e=arguments.length>0&&arguments[0]!==void 0?arguments[0]:"";const n=(arguments.length>1&&arguments[1]!==void 0?arguments[1]:!1)?"width":"height",t=w(`offset-${n}`);return{onBeforeEnter(a){a._parent=a.parentNode,a._initialStyle={transition:a.style.transition,overflow:a.style.overflow,[n]:a.style[n]}},onEnter(a){const i=a._initialStyle;a.style.setProperty("transition","none","important"),a.style.overflow="hidden";const u=`${a[t]}px`;a.style[n]="0",a.offsetHeight,a.style.transition=i.transition,e&&a._parent&&a._parent.classList.add(e),requestAnimationFrame(()=>{a.style[n]=u})},onAfterEnter:d,onEnterCancelled:d,onLeave(a){a._initialStyle={transition:"",overflow:a.style.overflow,[n]:a.style[n]},a.style.overflow="hidden",a.style[n]=`${a[t]}px`,a.offsetHeight,requestAnimationFrame(()=>a.style[n]="0")},onAfterLeave:r,onLeaveCancelled:r};function r(a){e&&a._parent&&a._parent.classList.remove(e),d(a)}function d(a){const i=a._initialStyle[n];a.style.overflow=a._initialStyle.overflow,i!=null&&(a.style[n]=i),delete a._initialStyle}}c("fab-transition","center center","out-in");c("dialog-bottom-transition");c("dialog-top-transition");const qe=c("fade-transition");c("scale-transition");c("scroll-x-transition");c("scroll-x-reverse-transition");c("scroll-y-transition");c("scroll-y-reverse-transition");c("slide-x-transition");c("slide-x-reverse-transition");const je=c("slide-y-transition");c("slide-y-reverse-transition");const Ge=G("expand-transition",J()),Je=G("expand-x-transition",J("",!0));export{B as V,Oe as a,Ne as b,Ge as c,we as d,Te as e,ze as f,pe as g,je as h,Je as i,qe as j};
