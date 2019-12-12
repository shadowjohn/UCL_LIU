using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Runtime.InteropServices;
using System.Reflection;
using System.Threading;
using System.Windows.Forms;
using System.ComponentModel;
using System.Threading;
using System.Web.Script.Serialization;
using utility;
namespace uclliu
{
    public class uclliu
    {
        myinclude my = new myinclude();
        //UserActivityHook actHook = new UserActivityHook();
        //public static extern int SetWindowsHookEx(int idHook, NativeStructs.HookProc lpfn, IntPtr hInstance, int threadId);
        public string VERSION = "0.1";
        public bool is_send_ucl = false;
        public bool flag_is_play_otherkey = false;
        public bool flag_is_shift_down = false;
        public bool is_DEBUG_mode = true;
        public string play_ucl_label = "";
        public string last_word_label_txt = "";
        public bool flag_is_win_down = false;
        public bool flag_is_capslock_down = false;
        public bool flag_is_play_capslock_otherkey = false;
        public bool flag_is_ctrl_down = false;
        public string same_sound_last_word = "";
        public bool is_need_use_pinyi = false;
        public List<string> ucl_find_data = new List<string>();
        Form1 f;
        public void show_sp_to_label(string data)
        {

        }
        public void use_pinyi(string data)
        {

        }
        public bool is_ucl()
        {
            return (f.btn_UCL.Text == "肥");
        }
        public bool is_hf()
        {
            return (f.btn_HALF.Text == "半");
        }
        public string widen(string data)
        {
            return data;
        }
        public void play_ucl(string thekey)
        {
            this.play_ucl_label = f.type_label.Text;
            //# 不可以超過5個字
            if (this.play_ucl_label.Length < 5)
            {
                this.play_ucl_label = string.Format("{0}{1}", this.play_ucl_label, thekey);
                this.type_label_set_text();
            }
        }
        public void toggle_hf()
        {
            string kind = f.btn_HALF.Text;
            switch (kind)
            {
                case "半":
                    f.btn_HALF.Text = "全";
                    break;
                default:
                    f.btn_HALF.Text = "半";
                    break;
            }
            //hf_label = self.get_child()
            //hf_label.modify_font(pango.FontDescription(GUI_FONT_22))
            this.toAlphaOrNonAlpha();
        }
        public void toAlphaOrNonAlpha()
        {
            if (f.btn_UCL.Text == "英" && f.btn_HALF.Text == "半")
            {
                f.Opacity = 0.2;
                f.TopMost = false;
                f.TopLevel = true;
            }
            else
            {
                f.Opacity = 1;
                //win.set_opacity( float(config["DEFAULT"]["ALPHA"]) )
                f.TopMost = true;
                f.TopLevel = true;
            }
        }
        public void toggle_ucl()
        {
            switch (f.btn_UCL.Text)
            {
                case "肥":
                    f.btn_UCL.Text = "英";
                    this.play_ucl_label = "";
                    this.type_label_set_text();                    
                    break;
                case "英":
                    f.btn_UCL.Text = "肥";
                    break;
            }
            this.debug_print("window_state_event_cb(toggle_ucl)");
            this.toAlphaOrNonAlpha();
        }
        public void debug_print(string data)
        {
            if (this.is_DEBUG_mode)
            {
                Console.WriteLine(data);
            }
        }
        public void type_label_set_text(string last_word_label_txt = "")
        {
            f.type_label.Text = this.play_ucl_label;
            if (this.play_ucl_label.Length > 0)
            {
                this.debug_print("ShowSearch");
                this.show_search();
            }
            f.word_label.Text = "";
            // 如果 last_word_label_txt 不是空值，代表有簡根或其他用字
            //word_label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
            if (this.last_word_label_txt != "")
            {
                f.word_label.Text = last_word_label_txt;
                //word_label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color("#007fff"));
            }
            //如果是短米，自動看幾個字展長
            /*if config["DEFAULT"]["SHORT_MODE"] == "1":
            _tape_label = type_label.get_label()
            _len_tape_label = len(_tape_label)
            #一字30
            if _len_tape_label == 0:
                type_label.set_visible(False)
            else:
                type_label.set_visible(True)
            type_label.set_size_request(int(float(config['DEFAULT']['ZOOM']) * 18 * _len_tape_label), int(float(config['DEFAULT']['ZOOM']) * 40))
*/

            string _word_label = f.word_label.Text;
            int _len_word_label = _word_label.Length;
            //一字30
            if (_len_word_label == 0)
            {
                f.word_label.Visible = false;
            }
            else
            {
                f.word_label.Visible = true;
            }
            //f.word_label.set_size_request(int(float(config['DEFAULT']['ZOOM']) * 15 * _len_word_label), int(float(config['DEFAULT']['ZOOM']) * 40))




        }
        public void show_search()
        {

        }
        public void toggle_half()
        {
            switch (f.btn_HALF.Text)
            {
                case "半":
                    f.btn_HALF.Text = "全";
                    break;
                case "全":
                    f.btn_HALF.Text = "半";
                    break;
            }
        }
        public void senddata(string data)
        {
            data = "肥仔的天下";
            //出字
            //From : https://burorly.pixnet.net/blog/post/10185692-c%23%E8%A7%A3%E6%B1%BA%E4%B8%AD%E6%96%87%E5%AD%97%E5%8D%A0%E7%94%A82%E5%80%8Bbyte%E9%95%B7%E5%BA%A6%E8%A8%88%E7%AE%97%E6%96%B9%E5%BC%8F
            //byte[] lineStr = System.Text.Encoding.UTF8.GetBytes(data);
            //int len = System.Text.Encoding.UTF8.GetByteCount(data);
            for (int i = 0; i < data.Length; i++)
            {
                string str = data.Substring(i, 1); // System.Text.Encoding.UTF8.GetString(lineStr, i,1);
                this.is_send_ucl = true;
                SendKeys.SendWait(str);
                //Thread.Sleep(50);
            }
        }

        public uclliu(ref Form1 _f)
        {
            f = _f;
            //f.Enabled = true;
            //f.btn_UCL.Text = "GG";
        }
    }
}
