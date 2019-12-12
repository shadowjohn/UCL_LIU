using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Runtime.InteropServices;

namespace uclliu
{
    public partial class Form1 : Form
    {
        //Allow console,
        //From : https://stackoverflow.com/questions/4362111/how-do-i-show-a-console-output-window-in-a-forms-application
        [DllImport("kernel32.dll", SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        static extern bool AllocConsole();

        private delegate int LowLevelKeyboardProcDelegate(int nCode, int
              wParam, ref KBDLLHOOKSTRUCT lParam);

        [DllImport("user32.dll", EntryPoint = "SetWindowsHookExA", CharSet = CharSet.Ansi)]
        private static extern int SetWindowsHookEx(
           int idHook,
           LowLevelKeyboardProcDelegate lpfn,
           int hMod,
           int dwThreadId);

        [DllImport("user32.dll")]
        private static extern int UnhookWindowsHookEx(int hHook);

        [DllImport("user32.dll", EntryPoint = "CallNextHookEx", CharSet = CharSet.Ansi)]
        private static extern int CallNextHookEx(
            int hHook, int nCode,
            int wParam, ref KBDLLHOOKSTRUCT lParam);

        const int WH_KEYBOARD_LL = 13;
        private int intLLKey;
        private KBDLLHOOKSTRUCT lParam;

        private struct KBDLLHOOKSTRUCT
        {
            public int vkCode;
            int scanCode;
            public int flags;
            int time;
            int dwExtraInfo;
        }
        public void log(string data)
        {
            //output_label.Text = data + " " + output_label.Text;
            Console.WriteLine(data);
        }

        private int LowLevelKeyboardProc(
            int nCode, int wParam,
            ref KBDLLHOOKSTRUCT lParam)
        {
            bool LShift = (lParam.vkCode == 160);
            bool RShift = (lParam.vkCode == 161);
            bool LCtrl = (lParam.vkCode == 162);
            bool LRtrl = (lParam.vkCode == 163);
            bool ESC = (lParam.vkCode == 27);
            bool LWin = (lParam.vkCode == 91);
            bool RWin = (lParam.vkCode == 92);
            bool CAPS = (lParam.vkCode == 20);
            bool BACK = (lParam.vkCode == 8);

            int ea = lParam.vkCode;
            bool keydown = (wParam == 256);
            bool keyup = (wParam == 257);

            int OK = 0;
            int NO = 1;
            int BK = -1;
            log("nCode:" + nCode.ToString());
            log("wParam:" + wParam.ToString());
            log("vkCode:" + lParam.vkCode.ToString());
            log("is_send_ucl:" + ucl.is_send_ucl.ToString());

            if (ucl.is_send_ucl == true)
            {
                //出字用
                ucl.is_send_ucl = false;
                return OK;
            }
            if (keydown && ucl.is_ucl() && ucl.play_ucl_label.Length >= 1 && ESC)
            {
                //如果是肥模式，且輸入的字>=1以上，按下 esc 鍵，會把字消除
                ucl.play_ucl_label = "";
                ucl.type_label_set_text();
                return NO;
            }
            if (keydown && (LWin || RWin))
            {
                ucl.flag_is_win_down = true;
                ucl.debug_print("Debug event A");
            }
            if (keyup && (LWin || RWin))
            {
                ucl.flag_is_win_down = false;
                ucl.debug_print("Debug event B");
            }
            if (keydown && (LShift || RShift))
            {
                //如果按著 shift 還用 滑鼠，不會切換 英/肥
                if (ucl.flag_is_shift_down == false)
                {
                    ucl.flag_is_play_otherkey = false;
                }
                ucl.flag_is_shift_down = true;
                ucl.debug_print("Debug event C");
            }
            if (keydown && CAPS)
            {
                ucl.flag_is_capslock_down = true;
                ucl.flag_is_play_capslock_otherkey = false;
                ucl.debug_print("Debug event E");
            }
            if (keydown && !CAPS)
            {
                ucl.flag_is_play_capslock_otherkey = true;
                ucl.debug_print("Debug event F");
            }
            if (keyup && CAPS)
            {
                ucl.flag_is_capslock_down = false;
                ucl.flag_is_play_capslock_otherkey = false;
                ucl.debug_print("Debug event E");
            }
            if (keydown && (!LShift && !RShift))
            {
                ucl.debug_print("Debug event D");
                ucl.flag_is_play_otherkey = true;
            }
            if (ucl.flag_is_capslock_down && ucl.flag_is_play_capslock_otherkey)
            {
                if (BACK && ucl.is_ucl() && ucl.play_ucl_label.Length >= 1)
                {
                    ucl.debug_print("Debug 2019-03-06 CapsLock + backspace");
                }
                else
                {
                    return OK;
                }
            }
            if (keyup && (LShift || RShift))
            {
                ucl.debug_print("Debug event G");
                //ucl.debug_print("event.MessageName:"+event.MessageName);
                //ucl.debug_print("ea:"+str(ea));
                //ucl.debug_print("event.KeyID:"+str(event.KeyID));
                //ucl.debug_print("flag_is_play_otherkey:"+str(flag_is_play_otherkey));
                //ucl.debug_print("flag_is_shift_down:"+str(flag_is_shift_down))        ;
                //ucl.debug_print("flag_is_capslock_down:"+str(flag_is_capslock_down));
                //ucl.debug_print("flag_is_play_capslock_otherkey:"+str(flag_is_play_capslock_otherkey));
                ucl.flag_is_shift_down = false;
                ucl.debug_print("Press shift");

                //# 不可是右邊的2、4、6、8      
                //# toAlphaOrNonAlpha()
                if (ucl.flag_is_play_otherkey == false && (ea > 40 || ea < 37))
                {
                    ucl.toggle_ucl();
                    ucl.debug_print("Debug15");
                    ucl.debug_print("Debug14");
                }
                return OK;
            }
            if (keydown && ea == 32 && ucl.flag_is_shift_down)
            {
                //# Press shift and space
                //# switch 半/全
                //ucl.hf_btn_click(hf_btn);
                btn_HALF.PerformClick(); //trigger click
                ucl.flag_is_play_otherkey = true;
                ucl.flag_is_shift_down = false;
                ucl.debug_print("Debug13");
                return NO;
            }
            if (ucl.is_ucl())
            {
                if (keydown && ucl.flag_is_win_down == true)
                {// # win key
                    return OK;
                }
                //#2018-05-05要考慮右邊數字鍵的 . 
                if (keydown && (ea >= 48 && ea <= 57) || (ea >= 96 && ea <= 105 || ea == 110))
                { // #0~9 .=110

                    if (ucl.ucl_find_data.Count >= 1 && Convert.ToInt32((char)(ea)) < ucl.ucl_find_data.Count)
                    {
                        //# send data        
                        string data = ucl.ucl_find_data[Convert.ToInt32((char)(ea))];
                        ucl.senddata(data);
                        //todo
                        //ucl.show_sp_to_label(data.decode('utf-8'));
                        //# 快選用的
                        //# print(data)        
                        ucl.debug_print("Debug12");
                        return NO;
                    }
                    else
                    {
                        if ((char)(ea).ToString().Length == 1 && ucl.is_hf() == false)
                        {
                            //#k = widen(event.Key)
                            //kac = ea
                            string k = ucl.widen(((char)(ea)).ToString());
                            //ucl.debug_print("event.Key to Full:%s %s" % (event.Key,k));
                            ucl.senddata(k);
                            ucl.debug_print("Debug11");
                            return NO;
                        }
                        ucl.debug_print("Debug10");
                        /*
                         #2017-10-24要考慮右邊數字鍵的狀況
                         #2018-05-05要考慮右邊數字鍵的 .
                         # ea==46 or (event.Key=="Decimal" and ea==46)
                         # 先出小點好了
                         */
                        if (ucl.is_hf() == false && (ea == 49 || ea == 50 || ea == 51 || ea == 52 || ea == 53 || ea == 54 || ea == 55 || ea == 56 || ea == 57 || ea == 47 || ea == 42 || ea == 45 || ea == 43 || ea == 48))
                        {
                            string k = ucl.widen(((char)(ea)).ToString());
                            ucl.senddata(k);
                            ucl.debug_print("Debug100");
                            return NO;
                        }
                        else
                        {
                            return OK;
                        }
                    }
                }
                if (keydown && ((ea >= 65 && ea <= 90) || (ea >= 97 && ea <= 122) || ea == 44 || ea == 46 || ea == 39 || ea == 91 || ea == 93))
                {
                    //# 這裡應該是同時按著SHIFT的部分
                    ucl.flag_is_play_otherkey = true;
                    if (ucl.flag_is_shift_down == true)
                    {
                        if (((char)(ea)).ToString().Length == 1 && ucl.is_hf() == false)
                        {
                            int kac = ea;
                            if (kac >= 65 && kac <= 90)
                            {
                                kac = kac + 32;
                            }
                            else
                            {
                                kac = kac - 32;
                            }
                            string k = ucl.widen(((char)(kac)).ToString());
                            //ucl.debug_print("285 event.Key to Full:%s %s" % (event.Key,k));
                            ucl.senddata(k);
                            ucl.debug_print("Debug9");
                            return NO;
                        }
                        ucl.debug_print("Debug8");
                        return OK;
                    }
                    else
                    {
                        //# Play ucl
                        //#print("Play UCL")
                        //#print(thekey)
                        ucl.play_ucl(((char)(ea)).ToString());
                        ucl.debug_print("Debug7");
                        return NO;
                    }
                }
                if (keydown && (ea == 8)) //: # ← backspace
                {
                    if (ucl.play_ucl_label.Length <= 0)
                    {
                        ucl.play_ucl_label = "";
                        ucl.play_ucl("");
                        ucl.debug_print("Debug6");
                        return OK;
                    }
                    else
                    {
                        //play_ucl_label = play_ucl_label[:-1]
                        ucl.play_ucl_label = ucl.play_ucl_label.Substring(0, ucl.play_ucl_label.Length-1);
                        ucl.type_label_set_text();
                        ucl.debug_print("Debug5");
                        return NO;
                    }
                }
                if (keydown && ea == 32) // : #空白
                {
                    //# Space
                    if (ucl.ucl_find_data.Count >= 1)
                    {
                        //#丟出第一個字                
                        string text = ucl.ucl_find_data[0];
                        if (ucl.same_sound_last_word == "")
                        {
                            ucl.same_sound_last_word = text;
                        }
                        if (ucl.is_need_use_pinyi)
                        {
                            //#使用同音字
                            ucl.debug_print("Debug use pinyi");
                            ucl.use_pinyi(ucl.same_sound_last_word);
                        }
                        else
                        {
                            ucl.senddata(text);
                            ucl.show_sp_to_label(text);
                        }
                        ucl.debug_print("Debug4");
                        return NO;
                    }
                    else if (ucl.ucl_find_data.Count == 0 && ucl.play_ucl_label.Length != 0)
                    {
                        //#無此字根時，按到空白鍵
                        ucl.debug_print("Debug11");
                        ucl.play_ucl_label = "";
                        ucl.ucl_find_data = new List<string>();
                        ucl.type_label_set_text();
                        return NO;
                    }
                    else
                    {
                        //#沒字時直接出空白
                        ucl.debug_print("Debug1");
                        if (ucl.is_hf() == false)
                        {
                            int kac = ea;
                            string k = ucl.widen(((char)(kac)).ToString());
                            ucl.senddata(k);
                            ucl.debug_print("Debug23");
                            return NO;
                        }
                        else
                        {
                            return OK;
                        }
                    }
                } // 空白
                else if (keydown && (ea == 58 || ea == 59 || ea == 123 || ea == 125 || ea == 40 || ea == 41 || ea == 43 || ea == 126 || ea == 33 || ea == 64 || ea == 35 || ea == 36 || ea == 37 || ea == 94 || ea == 38 || ea == 42 || ea == 95 || ea == 60 || ea == 62 || ea == 63 || ea == 34 || ea == 124 || ea == 47 || ea == 45))  //: # : ;｛｝（）＋～！＠＃＄％＾＆＊＿＜＞？＂｜／－
                {
                    //      #修正 肥/全 時，按分號、冒號只出半型的問題
                    if (ucl.is_hf() == false)
                    {
                        int kac = ea;
                        string k = ucl.widen(((char)(kac)).ToString());
                        ucl.senddata(k);
                        ucl.debug_print("Debug22");
                        return NO;
                    }
                    else
                    {
                        ucl.debug_print("Debug22OK");
                        return OK;
                    }
                }
                else
                {
                    return OK;
                }
                //Console.WriteLine("GG");
                //MessageBox.Show("gg1");
                //Console.WriteLine(nCode);
                //Console.WriteLine(wParam);
                //Console.WriteLine(lParam);
                //key down = 256
                //key up = 257
                //control = 163
                //shift 160
                /*
                int data = lParam.vkCode;
                // string keycode =  (char)lParam.KeyValue;
                if (data == 65 && keydown)
                {
                    ucl.senddata("肥");
                    return NO;
                }
                if (data >= 65 && data <= 65 + 26)
                {
                    log(((char)data).ToString());
                    //ok
                    return OK;
                }
                else
                {
                    log("Block:" + data.ToString());
                    return OK;
                }
                */
                /*

                bool blnEat = false;
                switch (wParam)
                {
                    case 256:
                    case 257:
                    case 260:
                    case 261:
                        //Alt+Tab, Alt+Esc, Ctrl+Esc, Windows Key
                        if (((lParam.vkCode == 9) && (lParam.flags == 32)) ||
                        ((lParam.vkCode == 27) && (lParam.flags == 32)) || ((lParam.vkCode ==
                        27) && (lParam.flags == 0)) || ((lParam.vkCode == 91) && (lParam.flags
                        == 1)) || ((lParam.vkCode == 92) && (lParam.flags == 1)) || ((true) &&
                        (lParam.flags == 32)))
                        {
                            blnEat = true;
                        }
                        break;
                }

                if (blnEat)
                    return 1;
                else return CallNextHookEx(0, nCode, wParam, ref lParam);
                */
            }
            else //is ucl
            {
                //ucl.debug_print("DDDDDDDDD: event.Key: " + event.Key + "\nDDDDDDDDD: event.KeyID: " + str(event.KeyID) + "\nDDDDDDDDD: event.MessageName: " +  event.MessageName )
                ucl.debug_print("flag_is_shift_down:" + ucl.flag_is_shift_down.ToString());
                ucl.debug_print("Debug3");
                ucl.debug_print(ea.ToString());
                if (keydown && ea == 13)
                {
                    return OK;
                }
                if (keydown && (ea == 91 || ea == 92))
                { // #winkey      
                    ucl.flag_is_win_down = true;
                    return OK;
                }
                //修正  在「英/全」的狀況，按下 esc (231 + 27 ) 無效的問題
                if (keydown && (ea == 231 || ESC))
                {
                    ucl.flag_is_win_down = false;
                    ucl.debug_print("Fix 23+27");
                    return OK;
                }
                if (keydown && ucl.flag_is_win_down == true) // : # win key
                {
                    ucl.flag_is_win_down = false;
                    return OK;
                }
                if (keydown && (ea == 231 || ea == 162 || ea == 163))
                {
                    ucl.flag_is_ctrl_down = true;
                    ucl.debug_print("Ctrl key");
                    return OK;
                }
                if (ucl.flag_is_ctrl_down == true)
                {
                    ucl.flag_is_ctrl_down = false;
                    return OK;
                }
                if (keydown && (LShift || RShift))
                {
                    ucl.flag_is_shift_down = true;
                    ucl.flag_is_play_otherkey = false;
                    ucl.debug_print("Debug331");
                }
                if (keydown && !LShift && !RShift)
                {
                    ucl.flag_is_play_otherkey = true;
                    ucl.debug_print("Debug332");
                }
                if (keyup && (LShift || RShift))
                {
                    ucl.debug_print("Debug333");
                    //#shift
                    ucl.flag_is_shift_down = false;
                    ucl.debug_print("Press shift");
                    if (ucl.flag_is_play_otherkey == false)
                    {
                        ucl.toggle_ucl();
                        ucl.debug_print("Debug315");
                    }
                    ucl.debug_print("Debug314");
                    return OK;
                }
                //debug_print("Debug3: %s" % (event.Transition))
                if (ea == 8 || ea == 20 || ea == 45 || ea == 46 || ea == 36 || ea == 33 || ea == 34 || ea == 35 || ea == 160 || ea == 161 || ea == 9 || ea == 37 || ea == 38 || ea == 39 || ea == 40 || ea == 231 || ea == 162 || ea == 163)
                { // #↑←→↓
                    return OK;
                }
                if (keydown && ((char)(ea)).ToString().Length == 1 && ucl.is_hf() == false)  // && event.Injected == 0 :
                {
                    //k = widen( str(chr(ea)) )
                    //senddata(k)
                    //數字變全型
                    return NO;
                }
                return OK;
            }
        }
        public void KeyboardHook(object sender, EventArgs e)
        {
            try
            {
                intLLKey = SetWindowsHookEx(WH_KEYBOARD_LL, new LowLevelKeyboardProcDelegate(LowLevelKeyboardProc),
                           System.Runtime.InteropServices.Marshal.GetHINSTANCE(
                           System.Reflection.Assembly.GetExecutingAssembly().GetModules()[0]).ToInt32(), 0);
            }
            catch (Exception ee)
            {
                Console.WriteLine(ee);
            }

        }

        private void ReleaseKeyboardHook()
        {
            intLLKey = UnhookWindowsHookEx(intLLKey);
        }

        //private void checkbox1_checkedchanged(object sender, eventargs e)
        //{
        //    if (checkbox1.checked)
        //        keyboardhook(this, e);
        //    else
        //        releasekeyboardhook();
        //        }
        //}
        uclliu ucl;
        private static Form1 form = null;
        public Form1()
        {
            InitializeComponent();
            //https://stackoverflow.com/questions/12983427/accessing-forms-controls-from-another-class
            form = this;
            ucl = new uclliu(ref form);
        }

        //令 form 可以移動 
        //From : https://stackoverflow.com/questions/1592876/make-a-borderless-form-movable
        private bool mouseDown;
        private Point lastLocation;

        private void Form1_MouseMove(object sender, MouseEventArgs e)
        {
            if (mouseDown)
            {
                this.Location = new Point(
                    (this.Location.X - lastLocation.X) + e.X, (this.Location.Y - lastLocation.Y) + e.Y);

                this.Update();
            }
        }

        private void Form1_MouseUp(object sender, MouseEventArgs e)
        {
            mouseDown = false;
        }
        private void Form1_MouseDown(object sender, MouseEventArgs e)
        {
            mouseDown = true;
            lastLocation = e.Location;
        }
        private void Form1_Load(object sender, EventArgs e)
        {
            //this.Size = new Size(400, 330);
            KeyboardHook(this, e);
            AllocConsole();
        }

        private void tableLayoutPanel1_MouseDown(object sender, MouseEventArgs e)
        {
            Form1_MouseDown(sender, e);
        }

        private void tableLayoutPanel1_MouseMove(object sender, MouseEventArgs e)
        {
            Form1_MouseMove(sender, e);
        }

        private void tableLayoutPanel1_MouseUp(object sender, MouseEventArgs e)
        {
            Form1_MouseUp(sender, e);
        }

        private void btn_X_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private void tableLayoutPanel1_Paint(object sender, PaintEventArgs e)
        {

        }

        private void btn_UCL_Click(object sender, EventArgs e)
        {
            ucl.toggle_ucl();
        }

        public void btn_HALF_Click(object sender, EventArgs e)
        {
            ucl.toggle_hf();
        }
    }
}
