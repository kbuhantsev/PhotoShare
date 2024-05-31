import{p as K,l as Q,J as W,a as me,o as r,c as V,w as n,b as l,e as B,F as C,r as U,m as P,av as ve,f as I,g as F,t as z,h as R,a9 as X,al as pe,z as y,C as A,E as he,n as Ve,a7 as ye,aw as T,ab as ge,ax as _e}from"./index-DsUmHdtM.js";import{h as ke,a as J,n as we,V as Ce}from"./VGrid-CxerTJ5w.js";import{V as be}from"./VSheet-BYO0Zu7S.js";import{c as Ie,a as Pe,b as Se,V as Y,d as xe}from"./VPagination-DQFkOWKI.js";import{m as Be,a as Fe,V as ze,f as Re}from"./forwardRefs-3yksCg8f.js";import{a as q,b as D,f as Ae,V as De}from"./index-IdDbBmo-.js";import{V as Ne,a as Me}from"./VRating-B7e2nfkd.js";import{V as He}from"./VSpacer-C925ELjg.js";import{V as $e}from"./VContainer-CqKgdPtt.js";import{c as Le,d as je,e as Ee,f as G,g as Oe,h as Ue,i as Te}from"./VTextField-CNcPHKi9.js";const Je=K({disabled:Boolean,modelValue:{type:Boolean,default:null},...Be()},"VHover"),qe=Q()({name:"VHover",props:Je(),emits:{"update:modelValue":e=>!0},setup(e,d){let{slots:p}=d;const u=W(e,"modelValue"),{runOpenDelay:s,runCloseDelay:i}=Fe(e,a=>!e.disabled&&(u.value=a));return()=>{var a;return(a=p.default)==null?void 0:a.call(p,{isHovering:u.value,props:{onMouseenter:s,onMouseleave:i}})}}}),Ge={key:1,class:"mt-1"},Ke={class:"px-4 mb-2"},Qe={class:"d-flex"},We={class:"text-grey ms-4"},Xe={class:"text-h4"},ca={__name:"PhotosList",props:{isLoading:Boolean,photos:Array},setup(e){const d=me(),p=u=>{console.log(u),d.push({name:"PhotoDetail",params:{photo_id:u}})};return(u,s)=>(r(),V($e,{class:"fill-height"},{default:n(()=>[l(ke,{class:"align-center text-center fill-height"},{default:n(()=>[e.isLoading?R("",!0):(r(),V(be,{key:0,class:"align-center"},{default:n(()=>[l(Ie,{items:e.photos,"items-per-page":6},{default:n(({items:i})=>[l(Pe,null,{default:n(()=>[(r(!0),B(C,null,U(i,a=>(r(),V(Se,{key:a.id,cols:"auto",class:"mx-auto my-12"},{default:n(()=>[l(qe,null,{default:n(({isHovering:f,props:g})=>{var h;return[l(q,P({lg:"4",elevation:14,title:a.raw.title,ref_for:!0},g),ve({default:n(()=>[a.raw.tags.length?(r(),V(D,{key:0},{default:n(()=>[I("div",Ke,[(r(!0),B(C,null,U(a.raw.tags,c=>(r(),V(Y,{key:c.id,class:"mr-2"},{default:n(()=>[F(z(c.name),1)]),_:2},1024))),128))])]),_:2},1024)):R("",!0),l(Ae,null,{default:n(()=>[l(J,{src:a.raw.secure_url,alt:a.raw.title,width:"250px",height:"300px"},null,8,["src","alt"])]),_:2},1024),l(D,null,{default:n(()=>[I("div",Qe,[l(Ne,{"model-value":a.raw.average_rating,color:"amber",density:"compact",size:"small","half-increments":"",readonly:""},null,8,["model-value"]),l(He),I("div",We,[l(Me,{color:"green",content:a.raw.comments.length},{default:n(()=>[l(we,{small:""},{default:n(()=>[F("mdi-comment")]),_:1})]),_:2},1032,["content"])])])]),_:2},1024),l(ze,{"model-value":f,class:"align-center justify-center",contained:""},{default:n(()=>[l(q,{class:"text-center"},{default:n(()=>[l(D,null,{default:n(()=>[I("p",Xe,z(a.raw.description),1)]),_:2},1024)]),_:2},1024),l(Ce,{variant:"outlined",onClick:c=>p(a.raw.id)},{default:n(()=>[F(" See more info")]),_:2},1032,["onClick"])]),_:2},1032,["model-value"])]),_:2},[(h=a.raw.owner)!=null&&h.avatar?{name:"append",fn:n(()=>[l(De,{size:"32"},{default:n(()=>{var c;return[a.raw.owner.avatar?(r(),V(J,{key:0,alt:a.raw.owner.username,src:a.raw.owner.avatar},null,8,["alt","src"])):(r(),B("span",Ge,z((c=a.raw.owner)==null?void 0:c.username),1))]}),_:2},1024)]),key:"0"}:void 0]),1040,["title"])]}),_:2},1024)]),_:2},1024))),128))]),_:2},1024)]),footer:n(({pageCount:i,prevPage:a,nextPage:f,setPage:g})=>{var h;return[(h=e.photos)!=null&&h.length&&i>1?(r(),V(xe,{key:0,length:i,"total-visible":5,rounded:"circle","onUpdate:modelValue":g,onPrev:a,onNext:f},null,8,["length","onUpdate:modelValue","onPrev","onNext"])):R("",!0)]}),_:1},8,["items"])]),_:1}))]),_:1})]),_:1}))}},Ye=K({chips:Boolean,counter:Boolean,counterSizeString:{type:String,default:"$vuetify.fileInput.counterSize"},counterString:{type:String,default:"$vuetify.fileInput.counter"},hideInput:Boolean,multiple:Boolean,showSize:{type:[Boolean,Number,String],default:!1,validator:e=>typeof e=="boolean"||[1e3,1024].includes(Number(e))},...Le({prependIcon:"$file"}),modelValue:{type:[Array,Object],default:e=>e.multiple?[]:null,validator:e=>X(e).every(d=>d!=null&&typeof d=="object")},...je({clearable:!0})},"VFileInput"),da=Q()({name:"VFileInput",inheritAttrs:!1,props:Ye(),emits:{"click:control":e=>!0,"mousedown:control":e=>!0,"update:focused":e=>!0,"update:modelValue":e=>!0},setup(e,d){let{attrs:p,emit:u,slots:s}=d;const{t:i}=pe(),a=W(e,"modelValue",e.modelValue,t=>X(t),t=>e.multiple||Array.isArray(e.modelValue)?t:t[0]??null),{isFocused:f,focus:g,blur:h}=Ee(e),c=y(()=>typeof e.showSize!="boolean"?e.showSize:void 0),N=y(()=>(a.value??[]).reduce((t,o)=>{let{size:_=0}=o;return t+_},0)),M=y(()=>T(N.value,c.value)),S=y(()=>(a.value??[]).map(t=>{const{name:o="",size:_=0}=t;return e.showSize?`${o} (${T(_,c.value)})`:o})),Z=y(()=>{var o;const t=((o=a.value)==null?void 0:o.length)??0;return e.showSize?i(e.counterSizeString,t,M.value):i(e.counterString,t)}),H=A(),$=A(),m=A(),ee=y(()=>f.value||e.active),L=y(()=>["plain","underlined"].includes(e.variant));function x(){var t;m.value!==document.activeElement&&((t=m.value)==null||t.focus()),f.value||g()}function ae(t){var o;(o=m.value)==null||o.click()}function te(t){u("mousedown:control",t)}function le(t){var o;(o=m.value)==null||o.click(),u("click:control",t)}function ne(t){t.stopPropagation(),x(),ge(()=>{a.value=[],_e(e["onClick:clear"],t)})}return he(a,t=>{(!Array.isArray(t)||!t.length)&&m.value&&(m.value.value="")}),Ve(()=>{const t=!!(s.counter||e.counter),o=!!(t||s.details),[_,oe]=ye(p),{modelValue:Ze,...se}=G.filterProps(e),re=Oe(e);return l(G,P({ref:H,modelValue:a.value,"onUpdate:modelValue":k=>a.value=k,class:["v-file-input",{"v-file-input--chips":!!e.chips,"v-file-input--hide":e.hideInput,"v-input--plain-underlined":L.value},e.class],style:e.style,"onClick:prepend":ae},_,se,{centerAffix:!L.value,focused:f.value}),{...s,default:k=>{let{id:b,isDisabled:w,isDirty:j,isReadonly:E,isValid:ue}=k;return l(Ue,P({ref:$,"prepend-icon":e.prependIcon,onMousedown:te,onClick:le,"onClick:clear":ne,"onClick:prependInner":e["onClick:prependInner"],"onClick:appendInner":e["onClick:appendInner"]},re,{id:b.value,active:ee.value||j.value,dirty:j.value||e.dirty,disabled:w.value,focused:f.value,error:ue.value===!1}),{...s,default:ie=>{var O;let{props:{class:ce,...de}}=ie;return l(C,null,[l("input",P({ref:m,type:"file",readonly:E.value,disabled:w.value,multiple:e.multiple,name:e.name,onClick:v=>{v.stopPropagation(),E.value&&v.preventDefault(),x()},onChange:v=>{if(!v.target)return;const fe=v.target;a.value=[...fe.files??[]]},onFocus:x,onBlur:h},de,oe),null),l("div",{class:ce},[!!((O=a.value)!=null&&O.length)&&!e.hideInput&&(s.selection?s.selection({fileNames:S.value,totalBytes:N.value,totalBytesReadable:M.value}):e.chips?S.value.map(v=>l(Y,{key:v,size:"small",text:v},null)):S.value.join(", "))])])}})},details:o?k=>{var b,w;return l(C,null,[(b=s.details)==null?void 0:b.call(s,k),t&&l(C,null,[l("span",null,null),l(Te,{active:!!((w=a.value)!=null&&w.length),value:Z.value,disabled:e.disabled},s.counter)])])}:void 0})}),Re({},H,$,m)}});export{da as V,ca as _};
