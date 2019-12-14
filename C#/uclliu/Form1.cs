using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
//using System.Linq;
using System.Text;
using System.Threading;
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

        [DllImport("user32.dll", EntryPoint = "SetWindowsHookEx", CharSet = CharSet.Ansi)]
        private static extern int SetWindowsHookEx(
           int idHook,
           LowLevelKeyboardProcDelegate lpfn,
           int hMod,
           int dwThreadId);

        [DllImport("user32.dll")]
        private static extern int UnhookWindowsHookEx(int hHook);

        [DllImport("user32.dll", EntryPoint = "CallNextHookEx", CharSet = CharSet.Auto)] //Ansi
        private static extern int CallNextHookEx(
            int hHook, int nCode,
            int wParam, ref KBDLLHOOKSTRUCT lParam);

        const int WH_KEYBOARD_LL = 13;
        private int intLLKey;
        private KBDLLHOOKSTRUCT lParam;

        //https://stackoverflow.com/questions/577411/how-can-i-find-the-state-of-numlock-capslock-and-scrolllock-in-net
        [DllImport("user32.dll", CharSet = CharSet.Auto, ExactSpelling = true, CallingConvention = CallingConvention.Winapi)]
        public static extern short GetKeyState(int keyCode);

        private struct KBDLLHOOKSTRUCT
        {
            public int vkCode;
            int scanCode;
            public int flags;
            int time;
            int dwExtraInfo;
        }


        private int LowLevelKeyboardProc(
            int nCode, int wParam,
            ref KBDLLHOOKSTRUCT lParam)
        {
            //return 0;            
            bool isCapsLock = (((ushort)GetKeyState(0x14)) & 0xffff) != 0;
            bool keydown = (wParam == 256);
            bool keyup = (wParam == 257);

            bool LShift = (lParam.vkCode == 160);
            bool RShift = (lParam.vkCode == 161);
            bool LCtrl = (lParam.vkCode == 162);
            bool RCtrl = (lParam.vkCode == 163);
            bool ESC = (lParam.vkCode == 27);
            bool LWin = (lParam.vkCode == 91);
            bool RWin = (lParam.vkCode == 92);
            bool CAPS = (lParam.vkCode == 20);
            bool BACK = (lParam.vkCode == 8);

            int ea = lParam.vkCode;
            /*
            if(ea >=65 && ea <= 65+26 && !isCapsLock)
            {
                ea += 32;
            }
            */

            int OK = 0; //同 pyhook 的 return True;
            int NO = 1; //同 pyhook 的 return False;
                        //int BK = -1;


            ucl.debug_print("nCode:" + nCode.ToString());
            ucl.debug_print("wParam:" + wParam.ToString());
            ucl.debug_print("vkCode:" + ea.ToString());
            ucl.debug_print("vkCode (char):" + ((char)(ea)).ToString());
            ucl.debug_print("vkCode GetType:" + lParam.GetType());
            ucl.debug_print("vkCode flags:" + lParam.flags);
            ucl.debug_print("vkCode GetHashCode:" + lParam.GetHashCode());
            ucl.debug_print("is_send_ucl:" + ucl.is_send_ucl.ToString());
            ucl.debug_print("flag_is_capslock_down:" + ucl.flag_is_capslock_down.ToString());
            ucl.debug_print("flag_is_play_capslock_otherkey:" + ucl.flag_is_play_capslock_otherkey.ToString());

            if (ucl.is_send_ucl == true)
            {
                //出字用
                ucl.is_send_ucl = false;
                return OK;
            }
            if (ucl.flag_is_gamemode)
            {
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
            if (keydown && (LCtrl || RCtrl))
            {
                ucl.flag_is_ctrl_down = true;
                ucl.debug_print("Ctrl key");
                return OK;
            }
            if (keyup && (LCtrl || RCtrl))
            {
                ucl.flag_is_ctrl_down = false;
                return OK;
            }
            if (keydown && ucl.flag_is_ctrl_down)
            {
                return OK;
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
                //107 +
                if (keydown && ucl.flag_is_shift_down == false && ((ea >= 48 && ea <= 57) || (ea >= 96 && ea <= 105) || ea == 110 || ea == 107 || ea == 109 || ea == 106 || ea == 111))
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
                        if (ucl.is_hf() == false && ucl.flag_is_shift_down == false && ((ea >= 96 && ea <= 105) || ea == 49 || ea == 50 || ea == 51 || ea == 52 || ea == 53 || ea == 54 || ea == 55 || ea == 56 || ea == 57 || ea == 47 || ea == 42 || ea == 45 || ea == 43 || ea == 48 || ea == 107 || ea == 110 || ea == 109 || ea == 106 || ea == 111))
                        {
                            int kac = ea;
                            switch (kac)
                            {
                                //修正肥/全，右邊數字鍵
                                case 106: //*
                                case 111: ///
                                case 110: //.
                                case 109: //-
                                case 107: //-
                                    kac -= 64;
                                    break;
                            }
                            if (kac >= 96 && kac <= 105)
                            {
                                //右邊的 0~9
                                kac -= 48;
                            }

                            string k = ucl.widen(((char)(kac)).ToString());
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

                //ea == 46 是 DELETE
                //(ea >= 97 && ea <= 122) a~z
                //|| ea == 39 右邊數字 →
                if (keydown && ((ea >= 65 && ea <= 90) || (ea >= 48 && ea <= 57) || ea == 44 || ea == 91 || ea == 93
                    || ea == 58 || ea == 59 || ea == 123 || ea == 125 || ea == 41 || ea == 43 || ea == 126 || ea == 64
                    || ea == 94 || ea == 42 || ea == 95 || ea == 60 || ea == 62 || ea == 63 || ea == 124 ||
                    ea == 47 || ea == 186 || ea == 187 || ea == 189 || ea == 191 || ea == 192 ||
                    ea == 219 || ea == 221 || ea == 222 || ea == 188 || ea == 190 || ea == 220 || ea == 222

                    ))
                {
                    //# 這裡應該是同時按著SHIFT的部分
                    ucl.flag_is_play_otherkey = true;

                    if (ucl.flag_is_shift_down == true)
                    {
                        ucl.debug_print("肥全按著 shift ");
                        if (((char)(ea)).ToString().Length == 1 && ucl.is_hf() == false)
                        {
                            int kac = ea;
                            //修正 c# 版無法偵測大小寫要作在這
                            if (kac >= 65 && kac <= 90 && !isCapsLock)
                            {
                                kac = kac + 32;
                            }
                            else if (kac >= 65 && kac <= 90 && isCapsLock)
                            {
                                //kac = kac;
                            }
                            switch (kac)
                            {
                                case 186: // : 
                                    kac = 58;
                                    break;
                                case 222: // "
                                    kac = 34;
                                    break;
                                case 220: // |
                                    kac = 124;
                                    break;
                                case 219: // {
                                    kac = 123;
                                    break;
                                case 221: // }
                                    kac = 125;
                                    break;
                                case 187: // =
                                    kac = 61;
                                    break;
                                case 188: // <
                                    kac = 60;
                                    break;
                                case 190: // >
                                    kac = 62;
                                    break;
                                case 189: // _
                                    kac = 95;
                                    break;
                                case 192: // ~
                                    kac = 126;
                                    break;
                                case 48: // )
                                    kac = 41;
                                    break;
                                case 49: // !
                                    kac = 33;
                                    break;
                                case 50: // @
                                    kac = 64;
                                    break;
                                case 51: // #
                                    kac = 35;
                                    break;
                                case 52: // $
                                    kac = 36;
                                    break;
                                case 53: // %
                                    kac = 37;
                                    break;
                                case 54: // ^
                                    kac = 94;
                                    break;
                                case 55: // &
                                    kac = 38;
                                    break;
                                case 56: // *
                                    kac = 42;
                                    break;
                                case 57: // (
                                    kac = 40;
                                    break;
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
                    else if (ucl.flag_is_shift_down == false && ucl.is_hf() == false &&
                    (ea == 58 || ea == 59 || ea == 123 || ea == 125 || ea == 41 || ea == 43 || ea == 126 || ea == 64
                    || ea == 94 || ea == 42 || ea == 95 || ea == 60 || ea == 62 || ea == 63 || ea == 124 ||
                    ea == 47 || ea == 186 || ea == 187 || ea == 189 || ea == 191 || ea == 192 || ea == 220))  //`: # : ;｛｝（）＋～！＠＃＄％＾＆＊＿＜＞？＂｜／－
                    {
                        //      #修正 肥/全 時，按分號、冒號只出半形的問題
                        int kac = ea;
                        switch (ea)
                        {
                            case 192: //`
                                kac -= 96;
                                break;
                            case 186: // ;                                
                                kac -= 127;
                                break;
                            case 220: //\
                                //kac = 92;
                                ucl.senddata("＼");
                                return NO;
                                break;
                            case 187: //+
                            case 188: //,
                            case 189: //-                            
                            case 190: //.
                            case 191: ///                           
                                kac -= 144;
                                break;
                        }
                        string k = ucl.widen(((char)(kac)).ToString());
                        ucl.senddata(k);
                        ucl.debug_print("Debug22");
                        return NO;
                    }
                    else if ((ea >= 65 && ea <= 91) || ea == 219 || ea == 221 || ea == 222 || ea == 188 || ea == 190)
                    {
                        //需a~z 、 [ ] ' ,
                        //# Play ucl
                        //#print("Play UCL")
                        //#print(thekey)
                        int kac = ea;
                        switch (kac)
                        {
                            case 188: // ,
                                kac = 44;
                                break;
                            case 190: // .
                                kac = 46;
                                break;
                            case 219: // [
                                kac = 91;
                                break;
                            case 221: // ]
                                kac = 93;
                                break;
                            case 222: //'
                                kac = 39;
                                break;
                        }
                        ucl.play_ucl(((char)(kac)).ToString());
                        ucl.debug_print("Debug7");
                        return NO;
                    }
                    else
                    {
                        //nothing to do
                        ucl.debug_print("對應不到功能");
                        return OK;
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
                        ucl.play_ucl_label = ucl.play_ucl_label.Substring(0, ucl.play_ucl_label.Length - 1);
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
                  //45  是 ins || ea == 45
                  //38 上 ea == 38 ||
                  //37 左 ea == 37 ||
                  //40 右 ea == 40 ||
                  //33 pageup
                  //34 pagedown
                  //35 end
                  //36 home
                  //186 ;
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
            else //is not ucl
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
                /*if (keydown && (LShift || RShift))
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
                */
                //debug_print("Debug3: %s" % (event.Transition))
                if (ea == 8 || ea == 20 || ea == 45 || ea == 46 || ea == 36 || ea == 33 || ea == 34 || ea == 35 || ea == 160 || ea == 161 || ea == 9 || ea == 37 || ea == 38 || ea == 39 || ea == 40 || ea == 231 || ea == 162 || ea == 163)
                { // #↑←→↓
                    return OK;
                }
                if (keydown && ((char)(ea)).ToString().Length == 1 && ucl.is_hf() == false)  // && event.Injected == 0 :
                {
                    int kac = ea;
                    //修正 c# 版無法偵測大小寫要作在這
                    //如果本來就是96~105，代表右邊的數字鍵
                    switch (kac)
                    {
                        case 96:
                        case 97:
                        case 98:
                        case 99:
                        case 100:
                        case 101:
                        case 102:
                        case 103:
                        case 104:
                        case 105:
                            kac -= 48;
                            break;
                        case 106:
                        case 107:
                        case 108:
                        case 109:
                        case 110:
                        case 111:
                            //右邊數字鍵，英全形
                            kac -= 64;
                            break;
                        case 186: // ;                                
                            kac -= 127;
                            break;
                        case 220: //\
                            kac -= 128;
                            ucl.senddata("＼");
                            return NO;
                            break;
                        case 219: //[
                            kac = 91;
                            break;
                        case 221: //]
                            kac = 93;
                            break;
                        case 222:
                            kac -= 183;
                            break;
                        case 187: //+
                        case 188: //,
                        case 189: //-                            
                        case 190: //.
                        case 191: ///                           
                            kac -= 144;
                            break;
                        case 192: //`
                            kac -= 96;
                            break;
                    }
                    if (kac >= 65 && kac <= 90 && !isCapsLock)
                    {
                        kac = kac + 32;
                    }
                    else if (kac >= 65 && kac <= 90 && isCapsLock)
                    {
                        //kac = kac;
                    }
                    string k = ucl.widen(((char)(kac)).ToString());
                    ucl.senddata(k);
                    ucl.debug_print("eng / full");
                    //數字變全形
                    return NO;
                }
                return OK;
            }

        }
        static LowLevelKeyboardProcDelegate hookProc;
        public void KeyboardHook(object sender, EventArgs e)
        {
            hookProc = new LowLevelKeyboardProcDelegate(LowLevelKeyboardProc);
            intLLKey = SetWindowsHookEx(WH_KEYBOARD_LL, hookProc,
                        System.Runtime.InteropServices.Marshal.GetHINSTANCE(
                        System.Reflection.Assembly.GetExecutingAssembly().GetModules()[0]).ToInt32(), 0);


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
            //如果超過畫面，要彈回來
            ucl.toAlphaOrNonAlpha();
            //換新位置了
            ucl.debug_print("肥米換新位置了，儲存");
            ucl.config["DEFAULT"]["X"] = this.Left.ToString();
            ucl.config["DEFAULT"]["Y"] = this.Top.ToString();
            ucl.saveConfig();
        }
        private void Form1_MouseDown(object sender, MouseEventArgs e)
        {
            mouseDown = true;
            lastLocation = e.Location;
        }
        private void Form1_Load(object sender, EventArgs e)
        {
            //檢查不能重複啟動
            if (!ucl.checkLockSuccess())
            {
                MessageBox.Show("肥米已執行了...");
                Application.Exit();
            }
            //載入 UCLLIU.ini
            ucl.loadConfig();
            //載入字根檔     
            ucl.loadJsonData();

            word_label.Text = "";
            type_label.Text = "";
            KeyboardHook(this, e);
            //修正一下畫面
            //

             
            /*this.TopLevel = true;
            this.TopLevel = false;
            this.TopLevel = true;
            this.TopMost = true;            
            this.TopMost = false;
            this.TopMost = true;
            */
            //Thread.Sleep(3000);
            btn_UCL.PerformClick();            
            btn_UCL.PerformClick();
            //起始不可以是 topmost ，在程式執行後，才置高，不然
            //首次切換輸入法時，會失去原始的焦點(如記事本)
            this.TopMost = true; 
            /*Thread.Sleep(1000);
            SendKeys.SendWait("+");
            Thread.Sleep(1000);
            SendKeys.SendWait("+");
            Thread.Sleep(1000);
            SendKeys.SendWait("+");
            Thread.Sleep(1000);
            SendKeys.SendWait("+");
            Thread.Sleep(1000);
            SendKeys.SendWait("+");
            Thread.Sleep(1000);
            SendKeys.SendWait("+");
            ucl.toAlphaOrNonAlpha();
            */
            //AllocConsole();            
        }

        private void LP_MouseDown(object sender, MouseEventArgs e)
        {
            Form1_MouseDown(sender, e);
        }

        private void LP_MouseMove(object sender, MouseEventArgs e)
        {
            Form1_MouseMove(sender, e);
        }

        private void LP_MouseUp(object sender, MouseEventArgs e)
        {
            Form1_MouseUp(sender, e);
        }

        private void btn_X_Click(object sender, EventArgs e)
        {
            ucl.debug_print("Bye Bye!");
            Application.Exit();
        }
               
        private void btn_UCL_Click(object sender, EventArgs e)
        {
            //點到 肥 或 英
            ucl.toggle_ucl();
        }

        public void btn_HALF_Click(object sender, EventArgs e)
        {
            //點到 半形 或 全形
            ucl.toggle_hf();
        }

        private void btn_gamemode_Click(object sender, EventArgs e)
        {
            //點到 正常模式 或 遊戲模式
            ucl.toggle_gamemode();
        }

    }
}
