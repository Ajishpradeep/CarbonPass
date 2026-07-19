import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
plt.rcParams.update({"font.size":13,"axes.edgecolor":"#444","axes.linewidth":0.8,
 "font.family":"DejaVu Sans","axes.grid":True,"grid.color":"#DDD","grid.linewidth":0.6})
INK="#1A3A4A"; ACC="#B8433A"; STE="#1A6B8A"; MIST="#9DB4C0"; GOLD="#8A6D1A"; GREY="#B8BFC4"

# ---- Chart A: what's in the scrap (carbon + money) ----
fig,ax=plt.subplots(1,2,figsize=(11,4.6))
lines=["firm_a\ncarbon","firm_b\ncarbon","firm_b\nSTAINLESS"]
co2=[758,1138,742]; money=[7.35,11.21,13.43]
cols=[STE,STE,ACC]
b1=ax[0].bar(lines,co2,color=cols); ax[0].set_ylabel("tCO$_2$e binned per year")
ax[0].set_title("Carbon in the scrap bin",color=INK,fontweight="bold")
for r,v in zip(b1,co2): ax[0].text(r.get_x()+r.get_width()/2,v+15,f"{v:,}",ha="center",fontsize=11)
b2=ax[1].bar(lines,money,color=cols); ax[1].set_ylabel("NT$ million binned per year")
ax[1].set_title("Money in the scrap bin",color=INK,fontweight="bold")
for r,v in zip(b2,money): ax[1].text(r.get_x()+r.get_width()/2,v+0.15,f"{v:.1f}",ha="center",fontsize=11)
fig.suptitle("The stainless line is the smallest product yet the biggest loss (39% of binned carbon on 24% of output)",
 fontsize=11.5,color="#333")
plt.tight_layout(rect=[0,0,1,0.94]); plt.savefig("chartA_waste.png",dpi=150,bbox_inches="tight"); plt.close()

# ---- Chart B: two levers, 80x apart ----
fig,ax=plt.subplots(figsize=(10,4.6))
labels=["Yield  9.1%->5% loss\n(MOVES the CBAM number)","Grid-aware load-shift\n(does NOT move it - indirect)"]
vals=[359,4.49]; cols=[ACC,MIST]
b=ax.barh(labels,vals,color=cols); ax.set_xlabel("tCO$_2$e per year (firm_a)")
for r,v in zip(b,vals): ax.text(v+5,r.get_y()+r.get_height()/2,f"{v:g} tCO$_2$e",va="center",fontsize=12,fontweight="bold")
ax.set_title("Two reduction levers, 80x apart in carbon",color=INK,fontweight="bold")
ax.text(359*0.5,0.0,"80x",ha="center",va="center",fontsize=22,color="white",fontweight="bold")
ax.invert_yaxis()
plt.tight_layout(); plt.savefig("chartB_levers.png",dpi=150,bbox_inches="tight"); plt.close()

# ---- Chart C: CBAM is a tariff on Taiwan's competitors ----
fig,ax=plt.subplots(figsize=(11,5))
c=["Philippines","Thailand","TAIWAN","Vietnam","No book ->\nfallback","India","China","Indonesia"]
v=[113.45,199.40,224.18,227.72,397.58,473.66,528.0,681.51]
cols=[MIST,MIST,ACC,MIST,GOLD,GREY,GREY,GREY]
b=ax.bar(c,v,color=cols); ax.set_ylabel("Buyer cost EUR / t of fasteners (2026, no data)")
ax.set_title("CN 7318 default by country of origin: Taiwan's is mild - CBAM prices its competitors' data poverty",
 color=INK,fontweight="bold",fontsize=12)
for r,val in zip(b,v): ax.text(r.get_x()+r.get_width()/2,val+8,f"EUR{val:,.0f}",ha="center",fontsize=10)
ax.axhline(224.18,color=ACC,ls="--",lw=1); 
plt.xticks(fontsize=10.5)
plt.tight_layout(); plt.savefig("chartC_competitors.png",dpi=150,bbox_inches="tight"); plt.close()

# ---- Chart D: the stainless hole ----
fig,ax=plt.subplots(figsize=(9,4.6))
lab=["EU default today\n(carbon-steel value 2.978 t)","Honest actual\n(CN 7221 fallback, 6.003 t)"]
euro=[224.18,451.90]; cols=[MIST,ACC]
b=ax.bar(lab,euro,color=cols,width=0.55); ax.set_ylabel("Buyer cost EUR / t")
for r,v in zip(b,euro): ax.text(r.get_x()+r.get_width()/2,v+8,f"EUR{v:,.0f}",ha="center",fontweight="bold")
ax.annotate("",xy=(1,451.9),xytext=(1,224.18),arrowprops=dict(arrowstyle="<->",color=INK,lw=1.5))
ax.text(1.05,338,"+EUR228/t\n= EUR296,006/yr\n(firm_b, 1,300 t)",fontsize=11,color=INK,va="center")
ax.set_title("Stainless fasteners get a carbon-steel default: honest reporting costs the buyer 2.0x more, so nobody reports",
 color=INK,fontweight="bold",fontsize=11.5)
plt.tight_layout(); plt.savefig("chartD_stainless.png",dpi=150,bbox_inches="tight"); plt.close()

# ---- Chart E: 4B on the excluded side of the wall ----
fig,ax=plt.subplots(figsize=(9.5,4.4))
m=["qwen3-vl 4B\n(laptop, offline, no GPU)","qwen3-vl 8B","InternVL3.5-8B\n(challenger)"]
acc=[100,100,66]; cols=[ACC,STE,GREY]
b=ax.bar(m,acc,color=cols,width=0.6); ax.set_ylabel("Field-level accuracy (%)"); ax.set_ylim(0,112)
for r,v,n in zip(b,acc,["336/336","288/288","111/168"]):
    ax.text(r.get_x()+r.get_width()/2,v+2,f"{v}%\n({n})",ha="center",fontsize=11,fontweight="bold")
ax.set_title("Reading a Traditional-Chinese utility bill across 6 phone-photo degradations",
 color=INK,fontweight="bold",fontsize=12)
plt.tight_layout(); plt.savefig("chartE_vlm.png",dpi=150,bbox_inches="tight"); plt.close()
print("charts done:")
import os
for f in sorted(os.listdir(".")):
    if f.endswith(".png"): print("  ",f,os.path.getsize(f))
