namespace uclliu
{
    partial class Form1
    {
        /// <summary>
        /// 設計工具所需的變數。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 清除任何使用中的資源。
        /// </summary>
        /// <param name="disposing">如果應該處置 Managed 資源則為 true，否則為 false。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form 設計工具產生的程式碼

        /// <summary>
        /// 此為設計工具支援所需的方法 - 請勿使用程式碼編輯器修改
        /// 這個方法的內容。
        /// </summary>
        public void InitializeComponent()
        {
            this.LP = new System.Windows.Forms.TableLayoutPanel();
            this.word_label = new System.Windows.Forms.Label();
            this.btn_UCL = new System.Windows.Forms.Button();
            this.btn_HALF = new System.Windows.Forms.Button();
            this.type_label = new System.Windows.Forms.Label();
            this.btn_X = new System.Windows.Forms.Button();
            this.btn_gamemode = new System.Windows.Forms.Button();
            this.btn_simple = new System.Windows.Forms.Button();
            this.LP.SuspendLayout();
            this.SuspendLayout();
            // 
            // LP
            // 
            this.LP.AutoSize = true;
            this.LP.CausesValidation = false;
            this.LP.CellBorderStyle = System.Windows.Forms.TableLayoutPanelCellBorderStyle.Inset;
            this.LP.ColumnCount = 7;
            this.LP.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 20F));
            this.LP.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 20F));
            this.LP.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 20F));
            this.LP.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 20F));
            this.LP.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 20F));
            this.LP.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 20F));
            this.LP.ColumnStyles.Add(new System.Windows.Forms.ColumnStyle(System.Windows.Forms.SizeType.Absolute, 20F));
            this.LP.Controls.Add(this.word_label, 3, 0);
            this.LP.Controls.Add(this.btn_UCL, 0, 0);
            this.LP.Controls.Add(this.btn_HALF, 1, 0);
            this.LP.Controls.Add(this.type_label, 2, 0);
            this.LP.Controls.Add(this.btn_X, 6, 0);
            this.LP.Controls.Add(this.btn_gamemode, 5, 0);
            this.LP.Controls.Add(this.btn_simple, 4, 0);
            this.LP.Dock = System.Windows.Forms.DockStyle.Fill;
            this.LP.GrowStyle = System.Windows.Forms.TableLayoutPanelGrowStyle.FixedSize;
            this.LP.Location = new System.Drawing.Point(0, 0);
            this.LP.Margin = new System.Windows.Forms.Padding(0);
            this.LP.Name = "LP";
            this.LP.RowCount = 1;
            this.LP.RowStyles.Add(new System.Windows.Forms.RowStyle(System.Windows.Forms.SizeType.Absolute, 35F));
            this.LP.Size = new System.Drawing.Size(592, 35);
            this.LP.TabIndex = 1;
            this.LP.MouseDown += new System.Windows.Forms.MouseEventHandler(this.LP_MouseDown);
            this.LP.MouseMove += new System.Windows.Forms.MouseEventHandler(this.LP_MouseMove);
            this.LP.MouseUp += new System.Windows.Forms.MouseEventHandler(this.LP_MouseUp);
            // 
            // word_label
            // 
            this.word_label.AutoSize = true;
            this.word_label.Font = new System.Drawing.Font("微軟正黑體", 18F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(136)));
            this.word_label.Location = new System.Drawing.Point(71, 2);
            this.word_label.Name = "word_label";
            this.word_label.Size = new System.Drawing.Size(14, 35);
            this.word_label.TabIndex = 5;
            this.word_label.Text = "word_label";
            this.word_label.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            this.word_label.MouseDown += new System.Windows.Forms.MouseEventHandler(this.LP_MouseDown);
            this.word_label.MouseMove += new System.Windows.Forms.MouseEventHandler(this.LP_MouseMove);
            this.word_label.MouseUp += new System.Windows.Forms.MouseEventHandler(this.LP_MouseUp);
            // 
            // btn_UCL
            // 
            this.btn_UCL.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.btn_UCL.FlatAppearance.BorderSize = 0;
            this.btn_UCL.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.btn_UCL.Font = new System.Drawing.Font("微軟正黑體", 15.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(136)));
            this.btn_UCL.Location = new System.Drawing.Point(2, 2);
            this.btn_UCL.Margin = new System.Windows.Forms.Padding(0);
            this.btn_UCL.Name = "btn_UCL";
            this.btn_UCL.Size = new System.Drawing.Size(20, 35);
            this.btn_UCL.TabIndex = 1;
            this.btn_UCL.Text = "肥";
            this.btn_UCL.UseVisualStyleBackColor = true;
            this.btn_UCL.Click += new System.EventHandler(this.btn_UCL_Click);
            // 
            // btn_HALF
            // 
            this.btn_HALF.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.btn_HALF.FlatAppearance.BorderSize = 0;
            this.btn_HALF.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.btn_HALF.Font = new System.Drawing.Font("微軟正黑體", 15.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(136)));
            this.btn_HALF.Location = new System.Drawing.Point(24, 2);
            this.btn_HALF.Margin = new System.Windows.Forms.Padding(0);
            this.btn_HALF.Name = "btn_HALF";
            this.btn_HALF.Size = new System.Drawing.Size(20, 35);
            this.btn_HALF.TabIndex = 2;
            this.btn_HALF.Text = "半";
            this.btn_HALF.UseVisualStyleBackColor = true;
            this.btn_HALF.Click += new System.EventHandler(this.btn_HALF_Click);
            // 
            // type_label
            // 
            this.type_label.AutoSize = true;
            this.type_label.Font = new System.Drawing.Font("微軟正黑體", 18F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(136)));
            this.type_label.Location = new System.Drawing.Point(49, 2);
            this.type_label.Name = "type_label";
            this.type_label.Size = new System.Drawing.Size(14, 35);
            this.type_label.TabIndex = 4;
            this.type_label.Text = "type_label";
            this.type_label.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            this.type_label.MouseDown += new System.Windows.Forms.MouseEventHandler(this.LP_MouseDown);
            this.type_label.MouseMove += new System.Windows.Forms.MouseEventHandler(this.LP_MouseMove);
            this.type_label.MouseUp += new System.Windows.Forms.MouseEventHandler(this.LP_MouseUp);
            // 
            // btn_X
            // 
            this.btn_X.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.btn_X.FlatAppearance.BorderSize = 0;
            this.btn_X.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.btn_X.Font = new System.Drawing.Font("微軟正黑體", 15.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(136)));
            this.btn_X.Location = new System.Drawing.Point(134, 2);
            this.btn_X.Margin = new System.Windows.Forms.Padding(0);
            this.btn_X.Name = "btn_X";
            this.btn_X.Size = new System.Drawing.Size(456, 35);
            this.btn_X.TabIndex = 3;
            this.btn_X.Text = "╳";
            this.btn_X.UseVisualStyleBackColor = true;
            this.btn_X.Click += new System.EventHandler(this.btn_X_Click);
            // 
            // btn_gamemode
            // 
            this.btn_gamemode.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.btn_gamemode.AutoSize = true;
            this.btn_gamemode.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.btn_gamemode.FlatAppearance.BorderSize = 0;
            this.btn_gamemode.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.btn_gamemode.Location = new System.Drawing.Point(112, 2);
            this.btn_gamemode.Margin = new System.Windows.Forms.Padding(0);
            this.btn_gamemode.Name = "btn_gamemode";
            this.btn_gamemode.Size = new System.Drawing.Size(20, 35);
            this.btn_gamemode.TabIndex = 6;
            this.btn_gamemode.Text = "正常模式";
            this.btn_gamemode.UseVisualStyleBackColor = true;
            this.btn_gamemode.Click += new System.EventHandler(this.btn_gamemode_Click);
            // 
            // btn_simple
            // 
            this.btn_simple.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.btn_simple.Location = new System.Drawing.Point(93, 5);
            this.btn_simple.Name = "btn_simple";
            this.btn_simple.Size = new System.Drawing.Size(14, 29);
            this.btn_simple.TabIndex = 7;
            this.btn_simple.Text = "簡";
            this.btn_simple.UseVisualStyleBackColor = true;
            this.btn_simple.Visible = false;
            // 
            // Form1
            // 
            this.AccessibleRole = System.Windows.Forms.AccessibleRole.Window;
            this.AutoSize = true;
            this.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.BackgroundImageLayout = System.Windows.Forms.ImageLayout.None;
            this.ClientSize = new System.Drawing.Size(592, 35);
            this.Controls.Add(this.LP);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.None;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "Form1";
            this.ShowIcon = false;
            this.ShowInTaskbar = false;
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Load += new System.EventHandler(this.Form1_Load);
            this.MouseDown += new System.Windows.Forms.MouseEventHandler(this.Form1_MouseDown);
            this.MouseMove += new System.Windows.Forms.MouseEventHandler(this.Form1_MouseMove);
            this.MouseUp += new System.Windows.Forms.MouseEventHandler(this.Form1_MouseUp);
            this.LP.ResumeLayout(false);
            this.LP.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion
        public System.Windows.Forms.TableLayoutPanel LP;
        public System.Windows.Forms.Button btn_X;
        public System.Windows.Forms.Button btn_UCL;
        public System.Windows.Forms.Button btn_HALF;
        public System.Windows.Forms.Label word_label;
        public System.Windows.Forms.Label type_label;
        public System.Windows.Forms.Button btn_gamemode;
        public System.Windows.Forms.Button btn_simple;
    }
}

