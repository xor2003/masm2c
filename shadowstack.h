	    class _STATE;

    class ShadowStack {
        struct Frame {
            bool init=false;
            const char *file=nullptr;
            size_t line=0;
            dd sp=0;
            dw cs=0;
            dd ip=0;
            dd value=0;
            dw *pointer_=nullptr;
            size_t addcounter=0;
            size_t remcounter=0;
            bool itwascall=false;
            size_t call_deep=0;
        };

        std::vector<Frame> m_ss;
        size_t m_current=0;
        bool m_itiscall=false;
        bool m_itisret=false;
        size_t m_deep=1;
    public:
        ShadowStack() : m_ss(0x10000)
        {}

        int m_needtoskipcall=0;
        bool m_active=true;
        bool m_forceactive=false;

        size_t m_currentdeep=0;

        void enable() {m_active=true;}
        void disable() {m_active=false;}
        void forceenable() {m_forceactive=true;}
        void forcedisable() {m_forceactive=false;}

        void push(_STATE *_state, dd value);

        void pop(_STATE *_state);

        void print(_STATE *_state);
        void print_frame(const Frame& f);

        void itiscall() {m_itiscall=true;}
        void itisret() {m_itisret=true;}
        bool itwascall(_STATE* _state);

        void decreasedeep();
        bool needtoskipcalls();
        size_t getneedtoskipcallndclean(){int ret = m_needtoskipcall; m_needtoskipcall = 0; return ret;}
        void noneedreturn(){--m_needtoskipcall;}

        // Drop every recorded frame below the given stack offset. Frames at
        // sp < floor sit in dead stack space (the live stack occupies
        // [sp, top]); interrupt handlers and synthesized sentinels leave such
        // frames behind, and the next real pop scan would miscount them as
        // uncontrolled pops.
        void clear_frames_below(dw sp_floor) {
            for (auto& f : m_ss) {
                if (f.init && f.sp < sp_floor) {
                    f.init = false;
                }
            }
        }

        struct SavedState {
            size_t m_current;
            bool m_itiscall;
            bool m_itisret;
            size_t m_deep;
            int m_needtoskipcall;
            size_t m_currentdeep;
        };
        SavedState save_state() const {
            return {m_current, m_itiscall, m_itisret, m_deep, m_needtoskipcall, m_currentdeep};
        }
        void restore_state(const SavedState& s) {
            m_current = s.m_current;
            m_itiscall = s.m_itiscall;
            m_itisret = s.m_itisret;
            m_deep = s.m_deep;
            m_needtoskipcall = s.m_needtoskipcall;
            m_currentdeep = s.m_currentdeep;
        }
    };

